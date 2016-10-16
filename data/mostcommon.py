import nltk, csv
from collections import Counter
corpus = []
cnt = Counter()

for file in nltk.corpus.brown.fileids():
    for word in nltk.corpus.brown.words(file):
        corpus.append(str(word))

for word in corpus:
    if word not in ".,;()-'\"?!``''--:":
        cnt[word] += 1

cnt = [[x[0]] for x in cnt.most_common()]

print cnt

with open("word_order.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(cnt)
