class State:
    def __init__(self):
        self.turns = []


    def clear(self):
        self.turns = []


    def next_turn(self, nlu_output):
        self.turns.append({
            'nlu_output': nlu_output,
            'query_result': None,
            'dm_output': [dict()],
        })


    def append_dm_output(self, dm_output):
        self.turns[-1]['dm_output'] =  dm_output


    def append_query_result(self, query_result):
        self.turns[-1]['query_result'] =  query_result


    def get_question(self):
        for i in range(len(self.turns)-2, -1, -1):
            for dm_output in self.turns[i]['dm_output']:
                if 'question' in dm_output:
                    return dm_output['question']
        return None


    def get_query_result(self):
        for i in range(len(self.turns)-2, -1, -1):
            if self.turns[i]['query_result'] is not None:
                return self.turns[i]['query_result']
        return ()


    def get_request(self):
        for i in range(len(self.turns)-2, -1, -1):
            if 'request' in self.turns[i]['nlu_output']:
                return self.turns[i]['nlu_output']['request']
        return None
