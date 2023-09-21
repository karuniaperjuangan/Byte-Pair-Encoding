with open("./ind_newscrawl_2016_10K-sentences.txt","r") as fp:
  file_text = fp.read()

list_line = file_text.split("\n")
list_line.pop()

list_sentence = []
for line in list_line:
  list_sentence.append(line.split('\t')[-1])

word_freqs = {}

for text in list_sentence:
    words = text.lower().split(" ")
    for word in words:
      if word_freqs.get(word) == None:
        word_freqs[word] = 1
      else:
        word_freqs[word] +=1


splits = {word: [char for char in word] for word in word_freqs.keys()}

def compute_pair_freqs(splits):
    pair_freqs = {}
    for word, freq in word_freqs.items():
        split = splits[word]
        if len(split) == 1:
            continue
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            if pair_freqs.get(pair) == None:
              pair_freqs[pair] = freq
            else:
              pair_freqs[pair] += freq
    return pair_freqs

pair_freqs = compute_pair_freqs(splits)

best_pair = ""
max_freq = None

for pair, freq in pair_freqs.items():
    if max_freq is None or max_freq < freq:
        best_pair = pair
        max_freq = freq


def merge_pair(a, b, splits):
    for word in word_freqs:
        split = splits[word]
        if len(split) == 1:
            continue

        i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                split = split[:i] + [a + b] + split[i + 2 :]
            else:
                i += 1
        splits[word] = split
    return splits

vocab = []

for word in word_freqs.keys():
    for letter in word:
        if letter not in vocab:
            vocab.append(letter)
vocab.sort()


vocab_size = 5000
merges = {}
while len(vocab) < vocab_size:
    pair_freqs = compute_pair_freqs(splits)
    best_pair = ""
    max_freq = None
    for pair, freq in pair_freqs.items():
        if max_freq is None or max_freq < freq:
            best_pair = pair
            max_freq = freq
    splits = merge_pair(*best_pair, splits)
    merges[best_pair] = best_pair[0] + best_pair[1]
    vocab.append(best_pair[0] + best_pair[1])

with open("./list_vocab.txt",'w') as vocab_file:
  for vocabulary in vocab:
    vocab_file.write(vocabulary+"\n")
  

def tokenize(text):
    pre_tokenized_text = text.lower().split(" ")
    splits = [[l for l in word] for word in pre_tokenized_text]
    for pair, merge in merges.items():
        for idx, split in enumerate(splits):
            i = 0
            while i < len(split) - 1:
                if split[i] == pair[0] and split[i + 1] == pair[1]:
                    split = split[:i] + [merge] + split[i + 2 :]
                else:
                    i += 1
            splits[idx] = split

    return sum(splits, [])


text_examples = [
    "Mantan Kadiv Propam Polri Irjen Ferdy Sambo resmi diberhentiakan secara tidak hormat sebagai Anggota Polri.",
    "Real Madrid berhasil menjadi kampiun Liga Champions 2021-2022 setelah menyudahi perlawanan sengit dari Liverpool.",
    "Pasar Kangen merupakan juga ajang kreativitas dan produktivitas dalam pengolahan pangan berbasis nilai-nilai local dan bahan-bahan pangan lokal.",
    "Pada zaman dahulu kala, di atas sebuah bukit kecil yang jauh dari pemukiman penduduk, di daerah Kalimantan Barat hiduplah seorang lelaki bernama Sambo.",
    "The Universal Declaration of Human Rights (UDHR) is an international document adopted by the United Nations General Assembly that enshrines the rights and freedoms of all human beings.",
    "Владимир Путин bermain tembak-tembakan bersama Pemimpin China bernama 习近平 dan Raja Arab, سلمان بن عبد العزیز آل سعود",
    "호복으로써 한복에 나타나는 몇 가지 특징이 있다. 기본적으로 활동성을 중시하며 딱 붙는 옷이 아니다."
]

for index,text in enumerate(text_examples):
  print("%d. "%(index+1),end="")
  print(tokenize(text),"\n")

