import nltk
import csv
import spacy
from collections import Counter

cnt = Counter()

en_model = spacy.load('en')

document = ""
for file in nltk.corpus.brown.fileids():
    #print document
    sentences = nltk.corpus.brown.words(file)
    for word in sentences:
        document += word + " "

assert "dad" in document

corpus = en_model(document)

for word in corpus:
    if str(word) not in u".!?,;:'\"--'``'''()1234567890":

        cnt[str(word.lemma_)] += 1

cnt = [[x[0]] for x in cnt.most_common()]

print cnt

with open("word_order.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(cnt)
