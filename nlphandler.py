import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp import StanfordNLPHandler


f = open('sample.txt', 'r', errors='ignore')

raw = f.read().lower()

nltk.download('brown')

nltk.download('punkt')
nltk.download('wordnet')

nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

ps = nltk.PorterStemmer()

def StemTokens(tokens):
    return [ps.stem(token) for token in tokens]

def Tokenizer(text):
    return StemTokens(LemNormalize(text))

GREETING_INPUTS = ('hello', 'hi', 'greetings', 'hey')
GREETING_RESPONSES = ('hello', 'hi', 'greetings', 'hey')

MISC_RESPONSES = ('Good to know', 'I\'m not quite sure I understand', 'OK, I\'ll keep that in mind', 'Interesting')

stanfordNLPHandler = StanfordNLPHandler()

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
           return random.choice(GREETING_RESPONSES)

def respond(user_response):
    global sent_tokens

    user_word_tokens = nltk.word_tokenize(user_response)

    response = ''
    user_response = user_response.lower()

    user_sent_tokens = nltk.sent_tokenize(user_response)
    sent_tokens += user_sent_tokens

    greeting_response = greeting(user_response)
    if greeting_response is not None:
        return greeting_response

    questions = []

    for user_sent_token in user_sent_tokens:
        is_question = stanfordNLPHandler.is_question(user_sent_token)
        if is_question:
            questions.append(user_sent_token)
        sent_response = stanfordNLPHandler.analyze(user_sent_token, is_question=is_question)
        if sent_response not in response:
            response += sent_response

    if response != '':
        response = 'OK I\'ll note that down. ' + response

    TfidfVec = TfidfVectorizer(tokenizer=Tokenizer, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if response == '' and (req_tfidf == 0):
        response += random.choice(MISC_RESPONSES)
    elif sent_tokens[idx] not in response:
        response += stanfordNLPHandler.set_capitals(sent_tokens[idx])

    for sent_token in questions:
        sent_tokens.remove(sent_token)

    return response

if __name__ == '__main__':
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
        else:
            flag = False
            botprint(BYE_MESSAGE)

