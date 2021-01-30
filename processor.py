import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from slackclient import SlackClient

SLACK_TOKEN = 'xoxb-1694387543250-1718543035664-OAr4r4vH0vGN4WJeobfXc8h1'

slack_client = SlackClient(SLACK_TOKEN)

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

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
           return random.choice(GREETING_RESPONSES)

def respond(user_response):
    global sent_tokens, word_tokens

    user_word_tokens = nltk.word_tokenize(user_response)
    # print(nltk.pos_tag(user_word_tokens, tagset='universal'))

    response = ''
    user_response = user_response.lower()
    hasNGword = False;
    ng_word_list = ["who","why","what","where","when","how","?"]
    for word in ng_word_list:
        if(word in user_response):
            hasNGword = True
    if(hasNGword):
        print("hasNGword")
        pass
    else:
        sent_tokens += nltk.sent_tokenize(user_response)
        word_tokens += nltk.word_tokenize(user_response)


    TfidfVec = TfidfVectorizer(tokenizer=Tokenizer, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if (req_tfidf == 0):
        response += 'Good to know'
    else:
        response += sent_tokens[idx]
    return response

def list_channels():
    channels_call = slack_client.api_call("conversations.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

if __name__ == '__main__':
    def botprint(response):
        print('Bot: %s' % response)

    INTRODUCTION = 'Hello! I am a personal chatbot. Ask me about anything!'
    BYE_MESSAGE = 'Goodbye! Thanks for chatting!'

    flag = True

    channels = list_channels()
    print(SLACK_TOKEN)
    if channels:
        print("Channels: ")
        for c in channels:
            print(c['name'] + " (" + c['id'] + ")")
    else:
        print("Unable to authenticate.")

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

