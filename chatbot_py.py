# -*- coding: utf-8 -*-
"""chatbot.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18SC6QpqPoq0BvG_J5BfWuCijPMEF7zLs
"""

import numpy as np
import nltk
import string
import random

from nltk.corpus.reader.tagged import word_tokenize
f=open("/content/human_chat.txt",'r',errors='ignore')
raw_doc=f.read()
raw_doc=raw_doc.lower()
nltk.download('punkt')
nltk.download('wordnet')
sent_tokens=nltk.sent_tokenize(raw_doc)
word_tokens=nltk.word_tokenize(raw_doc)

sent_tokens[:2]

word_tokens[:2]

lemmer=nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
  return[lemmer.lemmatize(token) for token in tokens]
remove_punct_dict=dict((ord(punct),None)for punct in string.punctuation) 
def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREET_INPUTS=("hello","hi","greeting","sup","what's up","hey",)
GREET_RESPONSES=["hi","hey","*nods*","hi there","hello","I am glad You are talking to me"]
def greet(sentence):
  for word in sentence.split():
    if word.lower() in GREET_INPUTS:
      return random.choice(GREET_RESPONSES)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
  robo1_response=''
  TfidfVec=TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
  tfidf=TfidfVec.fit_transform(sent_tokens)
  vals=cosine_similarity(tfidf[-1],tfidf)
  idx=vals.argsort()[0][-2]
  flat=vals.flatten()
  flat.sort()
  req_tfidf=flat[-2]
  if(req_tfidf==0):
    robo1_response=robo1_response+"I am sorry! I don't understand you"
    return robo1_response
  else:
    robo1_response=robo1_response+sent_tokens[idx]
    return robo1_response

flag=True
print("Bot:My name is hanoch.Let's have a converstion!Also,if you want to exit any time,just type Bye")
while(flag==True):
  user_response=input()
  user_response=user_response.lower()
  if(user_response!='bye'):
    if(user_response=='thanks'or user_response=='thank you'):
      flag=False
      print("Bot:You are welcome..")
    else:
      if(greet(user_response)!=None):
        print("Bot:"+greet(user_response))
      else:
         sent_tokens.append(user_response)
         word_tokens=word_tokens+nltk.word_tokenize(user_response)
         final_words=list(set(word_tokens))
         print("Bot:",end="")
         print(response(user_response))
         sent_tokens.remove(user_response)
  else:
    flag=False
    print("Bot:Goodbye! Take care <3")