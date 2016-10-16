from api_key import API_KEY
import spacy
import spacy.parts_of_speech as POS
import requests
from pattern.en import conjugate, pluralize, comparative, superlative

#Contains the relative frequency of all the words in a corpus, with the most frequently used word ranked "1"
def load_ranks():
    corpus = open("word_order.csv").readlines()
    print corpus[0:10]
    rank = {}

    for line in corpus:
        line = line.split(",")
        ranks[line[0]] = int(line[1][1:-1])

    return rank

ranks = load_ranks()

#The "reading level", or relative frequency we use to establish whether a word is "difficult"
relative_hard = 10000

#English model for
en_nlp = spacy.load('en')
word_endpoint = 'https://wordsapiv1.p.mashape.com/words/'
word_headers = {
  'X-Mashape-Key': API_KEY,
  'Accept': 'application/json',
}

pos_map = {
  'NOUN': 'noun',
  'ADJ': 'adjective',
  'ADV': 'adverb',
  'VERB': 'verb',
}

tag_map = {
 'VBD': 'p',
 'VBG': 'part',
 'VBN': 'ppart',
 'VBP': '1sg',
 'VBZ': '3sg',
}

def transform(doc_str):
  tups = tokenize(doc_str)
  return [translate(x) if is_hard(x) else x.orth_ for x in toks]
  
def translate(tok):
  syns = get_syn(tok)
  if len(syns) == 0:
    return tok.orth_
  syns_with_scores = [(get_score(syn), syn) for syn in syns]
  best = min(syns_with_scores)[1]
  return reconjugate(best, tok)

def tokenize(doc_str):
  return en_nlp(doc_str)

def get_syn(tok):
  lemma = tok.orth_
  
  res = requests.get(word_endpoint + lemma, headers=word_headers).json()
  syns = parse_syn(res, pos_map.get(tok.pos_, 'other'))
  return syns

def parse_syn(res, pos):
  res = res['results']
  for item in res:
    if item['partOfSpeech'] == pos:
      return item['synonyms']
  return []

def reconjugate(syn, tok):
  tag = tok.tag_
  if tag in tag_map:
    return conjugate(syn, tag_map[tag], parse=True)
  if tag == 'JJR' or tag == 'RBR':
    return comparative(syn)
  if tag == 'JJS' or tag == 'RBS':
    return superlative(syn)
  if tag.startswith('N') and tag.endswith('S'):
    return pluralize(syn)
  # do nothing
  return syn

def is_hard(tok):
  if len(tok.orth_) < 3:
    return False
  return get_score(tok.lemma_) > relative_hard

def get_score(tup):
  return rank[tup.lemma_]

## UNIT TESTS

def test():
  unhinged = tokenize(u"I am unhinged")[2]
  best = tokenize(u"This is the best")[3]
  used = tokenize(u"I was played like a flute")[2]

  #print tokenize(u"Merry has a little sheep")
  #print get_syn(unhinged)
  #print reconjugate("pretty", best)
  #print reconjugate("find", used)
  #print translate(unhinged)
  #print transform(u"Exhausted from reading, I closed my door and got in bed.")

  print is_hard((u'transpirating',))
  print is_hard((u'the',))
  print get_score((u'the',))

if __name__ == '__main__':
  test()
