from nltk.corpus import wordnet as wn


def word_relation(word1, word2): 
  relations = []
  redict = {"hypernym" : 0, "hyponym": 0, "none": 0}
  word1s = wn.synsets(word1)
  word2s = wn.synsets(word2)  
  for w1 in word1s:
    for w2 in word2s:
      relations.append(syns_relation(w1, w2))
      
  for r in relations:
    redict[r] = redict[r] + 1
    
  return redict

def syns_relation(word1, word2):  
  hypow1  = set([i for i in word1.closure(lambda s:s.hyponyms())])
  hyperw1 = set([i for i in word1.closure(lambda s:s.hypernyms())])

  hypow2  = set([i for i in word2.closure(lambda s:s.hyponyms())])
  hyperw2 = set([i for i in word2.closure(lambda s:s.hypernyms())])
  
  if (word2 in hypow1):
    #print (word1, " is hypernym of ", word2)
    return "hypernym"
  elif (word2 in hyperw1):
    #print (word1, " is hyponym of ", word2)
    return "hyponym"
  
  return "none"
    

def get_synonyms(ws):
  synonyms = []
  for w in ws:
    #print(w.name(), w.lemma_names())
    for l in w.lemmas():
      synonyms.append(l.name())  
  return synonyms  

  
def is_synonym(word1, word2):
  word1s = wn.synsets(word1)
  word2s = wn.synsets(word2)
  
  s1 = get_synonyms(word1s)
  s2 = get_synonyms(word2s)
  

  return word2 in s1

def get_relation(word1, word2):
  if word1 == word2:
    return "equal"
  
  is_syn = is_synonym(word1, word2)
  if is_syn:
    return "syn"
  
  rels = word_relation(word1, word2)
  if rels["hypernym"] + rels["hyponym"] == 0 : 
    return "none"
  
  if rels["hypernym"] > rels["hyponym"]: 
    return "hypernym"
  
  return "hyponym"
  
  


