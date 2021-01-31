import stanza
from pycorenlp import StanfordCoreNLP
import string

stanza.download('en')

nlp = stanza.Pipeline('en')
corenlp = StanfordCoreNLP('http://localhost:9000')

class Entity:
    def __init__(self, name, typex, status):
        self.name = name
        self.type = typex
        self.contexts = []
        self.status = status

    def add_context(self, context):
        if context not in self.contexts:
            self.contexts.append(context)

    def __str__(self):
        return self.name + ', ' + self.type + ', ' + self.status + '\n'


class StanfordNLPHandler:
    def __init__(self):
        self.entities = {}
        self.max_recur = 3

    def analyze(self, sentence, is_question=False, author=None):

        if is_question and len(list({'schedule', 'itinerary', 'agenda', 'timetable'}.intersection(set(sentence.split())))) > 0:
            doc = nlp(sentence)
            for entity in doc.entities:
                if entity.type == 'PERSON':
                    return self.schedule(entity.text, is_author=False)
            if author is not None:
                return self.schedule(author.lower(), is_author=True)

        doc = nlp(sentence)
        results = self.mem(doc)
        if not is_question and sentence not in results:
            results += sentence
            if results[-1:] not in string.punctuation:
                results += '. '
            else:
                results += ' '

        if not is_question:
            for entity in doc.entities:
                self.entities[entity.text] = self.entities.get(entity.text, Entity(entity.text, entity.type))
                self.entities[entity.text].add_context(sentence)
            if author is not None:
                author = author.lower()
                self.entities[author] = self.entities.get(author, Entity(author, 'PERSON'))
                self.entities[author].add_context(sentence)
        if results == '':
            return ''
        return self.set_capitals(results)

    def mem(self, doc, path=[]):
        results = ''
        if len(path) > self.max_recur:
            return ''
        for entity in doc.entities:
            for text in self.entities.get(entity.text, Entity(entity.text, entity.type)).contexts:
                if text not in results and text not in path:
                    results += text
                    if results[-1:] not in string.punctuation:
                        results += '. '
                    else:
                        results += ' '
                    results += self.mem(nlp(text), path+[text])
        return results

    def schedule(self, person, is_author):
        if person not in self.entities:
            return 'It looks like you don\'t have anything scheduled for now. ' if is_author else 'It looks like %s doesn\'t have anything scheduled for now. ' % person
        results = ''
        for context in self.entities[person].contexts:
            for entity in nlp(context).entities:
                if entity.type in ('DATE', 'TIME'):
                    results += context
                    if results[-1:] not in string.punctuation:
                        results += '. '
                    else:
                        results += ' '
        if results == '':
            return 'It looks like you don\'t have anything scheduled for now. ' if is_author else 'It looks like %s doesn\'t have anything scheduled for now. ' % person
        return results

    def has_entities(self, message):
        return len(nlp(message).entities) > 0

    def is_question(self, message):
        output = corenlp.annotate(message, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse',
        'outputFormat': 'json'
        })
        return '(ROOT\n  (SBARQ' in output['sentences'][0]['parse'] or '(ROOT\n  (SQ' in output['sentences'][0]['parse'] or '(NN' not in output['sentences'][0]['parse']

    def set_capitals(self, message):
        message = message.lower()
        doc = nlp(message)
        message = message.capitalize()
        for entity in doc.entities:
            if entity.type in ('PERSON', 'DATE', 'LOC', 'GPE'):
                message = message.replace(entity.text, entity.text.title())
        return message

if __name__ == '__main__':
    message = 'yes i see ok'
    output = corenlp.annotate(message, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse',
        'outputFormat': 'json'
        })
    print(output['sentences'][0]['parse'])