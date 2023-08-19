import nltk


class NLUnderstanding:
    def __init__(self):
        sentlist = []
        with open('nlu/tagged_sentences', 'r') as infile:
            tagged = infile.readlines()

            for y in tagged:
                sentence = []
                groups = y.split()
                for x in groups:
                    spl = x.split('/')
                    pair = spl[0], spl[1]
                    sentence.append(pair)

                sentlist.append(sentence)
        
        _POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
        t1 = nltk.data.load(_POS_TAGGER)
        t2 = nltk.UnigramTagger(sentlist, backoff=t1)

        tagged_punc = [ (r'\"', ':'), (r'\?', 'QM'),(r'\.', 'EOS') ]
        self.tagger = nltk.RegexpTagger(tagged_punc, backoff=t2)


    def process(self, utterance):
        tokenized = nltk.word_tokenize(utterance)
        tagged = self.tagger.tag(tokenized)
        
        keys = [t[1] for t in tagged]
        values = [t[0] for t in tagged]
        paires = dict(zip(keys, values))

        response = dict()
        if 'BYE' in keys: return [{'command': 'exit'}]
        if 'RESTART' in keys: return [{'command': 'clear'}]

        if 'KW_MOVIE' in keys: response['request'] = 'title'
        if 'KW_DIRECTOR' in keys: response['request'] = 'director'
        if 'GNRE' in keys: response['genre'] = paires['GNRE'].capitalize()
        if 'CD' in keys: response['count'] = paires['CD']
        if 'JJ' in keys: response['order'] = paires['JJ']

        if 'IN' in keys:
            try:
                ind = keys.index('IN')
                if (keys[ind], keys[ind+1], keys[ind+2]) == ('IN', 'NNP', 'NNP') and values[ind] != 'from':
                    response['actor'] = values[ind+1].capitalize() + ' ' + values[ind+2].capitalize()
            except: pass

        if 'DT' in keys:
            try:
                ind = keys.index('DT')
                if (keys[ind], keys[ind+1]) == ('DT', 'NNP') and len(keys) > 3:
                    response['title'] = values[ind+1].capitalize()
            except: pass

        if len(keys) == 1: response['response'] = values[0]

        if len(response) == 1 and 'response' not in response:
            response = {}
        
        return [response]
