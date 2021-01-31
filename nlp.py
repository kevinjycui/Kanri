import stanza
from pycorenlp import StanfordCoreNLP

stanza.download('en')

nlp = stanza.Pipeline('en')
corenlp = StanfordCoreNLP('http://localhost:9000')


class StanfordNLPHandler:
    def __init__(self):
        self.people = {}
        self.datetimes = {}

    def analyze(self, sentence, is_question=False, author=None):
        doc = nlp(sentence)
        results = self.mem(doc)
        if not is_question and sentence not in results:
            results += sentence + '. '
        if not is_question:
            for entity in doc.entities:
                if entity.type == 'DATE' or entity.type == 'TIME':
                    self.datetimes[entity.text] = self.datetimes.get(entity.text, []) + [sentence]
                elif entity.type == 'PERSON':
                    self.people[entity.text] = self.people.get(entity.text, []) + [sentence]
            if author is not None:
                author = author.lower()
                self.people[author] = self.people.get(author, []) + [sentence]
        if results == '':
            return ''
        return self.set_capitals(results)

    def mem(self, doc):
        results = ''
        for entity in doc.entities:
            if entity.type == 'DATE' or entity.type == 'TIME':
                for text in self.datetimes.get(entity.text, []):
                    if text not in results:
                        results += text + '. '
            if entity.type == 'PERSON':
                for text in self.people.get(entity.text, []):
                    if text not in results:
                        results += text + '. '
        return results

    def is_question(self, message):
        output = corenlp.annotate(message, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse',
        'outputFormat': 'json'
        })
        return '(ROOT\n  (SBARQ' in output['sentences'][0]['parse'] or '(ROOT\n  (SQ' in output['sentences'][0]['parse']

    def set_capitals(self, message):
        message = message.lower()
        doc = nlp(message)
        message = message.capitalize()
        for entity in doc.entities:
            if entity.type in ('PERSON', 'DATE', 'LOC', 'GPE'):
                message = message.replace(entity.text, entity.text.title())
        return message