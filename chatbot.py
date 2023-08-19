from time import sleep
from nlu import NLUnderstanding
from dm import DialogManager
from nlg import nlg

utterances = (
    'I want to watch action movie with Keanu Reeves',
    '2',
    'movies about love',
    'movies from DC Studios',
    'List 5 most popular movies',
    'who directed the Inception',
    'movies count with Aaa Bbb',
    'movies count with Nicolas Cage',
    'no',
    'bye',
)

print('\n######################################################################################################################################################################'*20, '\n\n\n\n')
nlu = NLUnderstanding()
dialog_manager = DialogManager()


GREETING = "Hi, I'm movie recommendation dialog system. \n\tJust tell me your preferences and I'll try to find movies you'd like"
print('Bot: ', GREETING)
i = 0
try:
    # utterance = input('User:  ')
    utterance = utterances[i]
    print('\nUser: ', utterances[i])
    while utterance is not None:
        if len(utterance) == 0:
            utterance = input("Bot:  Please, write your response \nUser:  ")
            continue
        
        try:
            #  NLU processing
            nlu_out = nlu.process(utterance)
            print('DEBUG nlu: ', nlu_out)

            #  Dialog manager processing
            dm_out = dialog_manager.input(nlu_out)
            print('DEBUG dm: ', dm_out)
            
            #  Generate response to user
            output = nlg.process(nlu_out, dm_out)
        except Exception as e:
            print('DEBUG: ', e)
            dialog_manager.state.clear()
            output = "An exception occured. Let's start from scratch"
        
        #  Provide response to user
        print('Bot: ', output)
        
        #  Decide whether to continue
        for dict in nlu_out:
            if dict.get('command') == 'exit':
                print('Bot:  Bye!)')
                sleep(3)
                exit()
        
        #Get user input
        # utterance = input('User:  ')
        i += 1
        utterance = utterances[i]
        print('\nUser: ', utterances[i])
except Exception as e:
    print('An exception occured:', e)
    sleep(5)
    exit()