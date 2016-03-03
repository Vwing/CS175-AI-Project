
# coding: utf-8

# In[1]:

import csv
import re
import pandas as pd
import random
import copy
import nltk

NAME = "fleep"
GENDER = "M"
CLASS = "hunter"
RACE = "dwarf"

quests = pd.read_csv("quests.csv")
#print(list(quests.columns.values))
details = quests.Details
rawStr = ""
for d in details:
    rawStr += str(d)


# In[2]:

def get_ran_word(cfdist,word,sampleNum):
    d = copy.copy(cfdist[word])
    words = [None] * sampleNum
    for i in range(sampleNum):
        words[i] = d.max();
        del(d[words[i]]);
    return random.choice(words)

def generate_ran_sentence(cfdist, word, num=15):
    for i in range(num):
        print(word + " ")
        #print word + " "
        word = get_ran_word(cfdist,word,3)
        
def format_simple(document):
    doc = document.lower()                                           #convert to lower case
    doc = re.sub(r'[\.\?\{\}\[\]\\\|\(\)!,:\'-;\$\"]','',doc)         #remove punctuations
    doc = re.sub(r'[\s]+',' ', doc)                                  #remove whitespace clumps
    doc =  doc.strip()                                               #remove trailing whitespace
    return doc

def replace_variables(document):
    doc = document.lower()
    if GENDER == "M":
        doc = re.sub(r'\$g(.*):(.*);',r'\g<1>',doc)
    else:
        doc = re.sub(r'\$g(.*):(.*);',r'\g<2>',doc)
    doc = re.sub(r'\$c',CLASS,doc)
    doc = re.sub(r'\$n',NAME,doc)
    doc = re.sub(r'\$r',RACE,doc)
    return doc
    
def format_simple_keep_punctuation(document):
    doc = document.lower()                                           #convert to lower case
    doc = re.sub(r'[\\\|]','',doc)                                  #remove unneeded punctuations
    doc = re.sub(r'([\.\?\{\}\[\]\(\)!,:-;\$\"])',r' \g<1> ',doc)           #put spaces between tagged punctuations
    doc = re.sub(r'[\s]+',' ', doc)                                  #remove whitespace clumps
    doc =  doc.strip()                                               #remove trailing whitespace
    return doc


# In[3]:

rawStr = replace_variables(rawStr)
rawStr = format_simple_keep_punctuation(rawStr)
#tokens = nltk.word_tokenize(rawStr)
tokens = rawStr.split(' ')
text = nltk.Text(tokens)


# In[93]:

postag = nltk.pos_tag(text)
#tag_fd = nltk.FreqDist(tag for (word, tag) in postag)


# In[5]:

#print(tag_fd.most_common())


# In[99]:

from nltk import PCFG
from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
from operator import itemgetter

nonterms = {".",",",r"PRP$",":","$","\'\'", "(", ")", "CC", "CD", "DT", "EX", "FW", "IN"}
nonpos = {"i", "\""}
#test = {"NN","JJ","JJR","MD","RB","VB","RBS","RBR","UH", "VBP", "VBZ", "WDT", "CC", "NNS", "PRP", "VBN", "EX"}
postags = postag
postags.sort(key=itemgetter(1))
my_grammar = """
  S -> COL CD N
  N -> JJ NN FR NNP
  N -> JJ NN
  N -> NN
  COL -> 'Collect' | 'Gather'
  FR -> 'from'
"""
for x in range(len(postags)):
    postags[x] = (postags[x][0].replace(("\'", "\\\'")), postags[x][1])
my_grammar += "  " + "\n  ".join([(r"CD -> '" + str(num) + r"'") for num in range(1,6)])
my_grammar += "\n  " + "\n  ".join([(b + r" -> '" + a + r"'") for (a,b) in postags if b not in nonterms and a not in nonpos])
#for (a,b) in postags:
#    if b not in nonterms and a not in nonpos:
#        if a == "you'll" and b not in test:
#            print(b +": " + a + " - " + b[0])

grammar = CFG.fromstring(my_grammar)
print(grammar.productions())

for sentence in generate(grammar, n=100):
    print(' '.join(sentence))

#print(grammar)
#grammar += "\n\tN -> 'cat'"
#print(grammar)

#print(dir(CFG))
#print("\n")
#print(grammar.productions)

