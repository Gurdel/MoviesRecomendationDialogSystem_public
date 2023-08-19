from dbi import dbi
from dm.state import State


class DialogManager:
    def __init__(self):
        self.pending_question = None
        self.state = State()
        self.dbi = dbi
        self.MAX_RESULT_COUNT = 10
                    
    
    def input(self, nlu_output):
        self.state.next_turn(nlu_output)
        dm_output = []

        for d in nlu_output:
            if 'request' in d:
                dm_output.append(self.request(d))
            elif 'command' in d:
                dm_output.append(self.command(d))
            elif 'response' in d:
                dm_output.append(self.response(d))
            else:
                dm_output.append(dict())
        
        self.state.append_dm_output(dm_output)
        return dm_output
    

    def request(self, nlu_output):
        if nlu_output['request'] in (
            'title',
            'actor',
            'director',
            'year',
        ):
            result = self.dbi.execute_general_query(nlu_output)
            self.state.append_query_result(result)

            if not result:
                return {'list': 0}

            if len(result) > self.MAX_RESULT_COUNT:
                if nlu_output['request'] == 'title':
                    return {'list':len(result), 'question':'HOW_MANY'}
                return {'list':len(result), 'question':'TO_LIST'}
            
            return {'print':nlu_output['request'], 'results':result}



    def command(self, nlu_output):
        if nlu_output['command'] == 'exit':
            return {'print': 'exit'}
        
        if nlu_output['command'] == 'clear':
            self.state = State()
            return {'print': 'ok'}
    

    def response(self, nlu_output):
        question = self.state.get_question()

        if question == 'HOW_MANY':
            if not nlu_output['response'].isnumeric():
                return {'print':'continue'}
            count = int(nlu_output['response'])
            return {'print':'title', 'results':self.state.get_query_result()[:count]}

        if question == 'TO_LIST':
            response = nlu_output['response']

            if 'no' in response.lower():
                return {'print':'continue'}
        
            result = self.state.get_query_result()

            if len(result) > self.MAX_RESULT_COUNT:
                return {'list':len(result), 'question':'HOW_MANY'}
            
            return {'print':self.state.get_request(), 'results':result}

            
