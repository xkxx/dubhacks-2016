from api_key import API_KEY
import spacy
import spacy.parts_of_speech as POS
import requests

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

def tokenize(doc_str):
  doc = en_nlp(doc_str)
  return [(x.orth_, x.lemma_, pos_map.get(x.pos_, 'other')) for x in doc]

def get_syn(tup):
  (word, lemma, pos) = tup
  
  res = requests.get(word_endpoint + lemma, headers=word_headers).json()
  syns = parse_syn(res, pos)
  return syns

def parse_syn(res, pos):
  res = res['results']
  for item in res:
    if item['partOfSpeech'] == pos:
      return item['synonyms']
  return []
  
## UNIT TESTS

def test():
  print tokenize(u"Merry has a little sheep")
  print get_syn(('unhinged', 'unhinged', 'adjective'))

if __name__ == '__main__':
  test()
