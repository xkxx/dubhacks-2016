from api_key import API_KEY
import spacy, csv, requests
import spacy.parts_of_speech as POS
import requests
from pattern.en import conjugate, pluralize, comparative, superlative

#Uses a csv file formatted as "word, line number"\n. Loads said csv file into a dictionary
def load_ranks():
    rank = {}
    with open("../data/word_order.csv") as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            index += 1
            rank[row[0]] = index
    return rank

ranks = load_ranks()


#The "reading level", or relative frequency we use to establish whether a word is "difficult"
relative_hard = 100

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
  print 'tokenizing ...'
  toks = tokenize(doc_str)
  print 'tokenizing done'
  return ' '.join([translate(x) if is_hard(x) else x.orth_ for x in toks])

def translate(tok):
  syns = get_syn(tok)
  if len(syns) == 0:
    return tok.orth_
  syns_with_scores = [(get_score(syn), syn) for syn in syns]
  best = min(syns_with_scores)
  print 'original', tok.orth_, 'score', get_score(tok.lemma)
  print 'replacement', syn, 'score', get_score(syn)
  if get_score(syn) >= get_score(tok.lemma_):
    return tok.orth_
  return reconjugate(best[1], tok)

def tokenize(doc_str):
  return en_nlp(doc_str)

def get_syn(tok):
  lemma = tok.orth_

  res = requests.get(word_endpoint + lemma, headers=word_headers).json()
  syns = parse_syn(res, pos_map.get(tok.pos_, 'other'))
  return syns

def parse_syn(res, pos):
  res = res.get('results', [])
  for item in res:
    if item['partOfSpeech'] == pos:
      return item.get('synonyms', [])
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

def get_score(word):
  return ranks.get(word, 10001)

## UNIT TESTS

def test():
  unhinged = tokenize(u"I am unhinged")[2]
  best = tokenize(u"This is the best")[3]
  used = tokenize(u"I was played like a flute")[2]
  transpirating = tokenize(u'transpirating')[0]
  the = tokenize(u'the')[0]

  print tokenize(u"Merry has a little sheep")
  print get_syn(unhinged)
  print reconjugate("pretty", best)
  print reconjugate("find", used)
  print translate(unhinged)
  sent = u"Hidden from unhinged reading, I closed my door and got in bed."
  sent_toks = tokenize(sent)
  print "is miniscule hard?"
  print is_hard(sent_toks[2])
  print transform(sent)

  print is_hard(transpirating)
  print is_hard(the)
  print get_score('the')

if __name__ == '__main__':
  test()
