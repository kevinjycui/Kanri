import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


f = open('sample.txt', 'r', errors='ignore')

raw = f.read().lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ('hello', 'hi', 'greetings', 'hey')
GREETING_RESPONSES = ('hello', 'hi', 'greetings', 'hey')

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def respond(user_response):
    response = ''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if (req_tfidf == 0):
        response += 'Sorry, I don\'t understand... can you rephrase that?'
    else:
        response += sent_tokens[idx]
    return response

def botprint(response):
    print('Bot: %s' % response)

INTRODUCTION = 'Hello! I am a personal chatbot. Ask me about anything!'
BYE_MESSAGE = 'Goodbye! Thanks for chatting!'

flag = True

botprint(INTRODUCTION)

while flag:
    user_input = input().lower()
    if user_input != 'bye':
        greeting_response = greeting(user_input)
        if greeting_response is not None:
            botprint(greeting_response)
        else:
            botprint(respond(user_input))
            sent_tokens.remove(user_input)
    else:
        flag = False
        botprint(BYE_MESSAGE)

