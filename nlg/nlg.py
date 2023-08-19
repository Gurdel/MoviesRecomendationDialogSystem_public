import os
import random


BASE_PATH = 'nlg/templates'


def process(nlu_output, dm_output):
    nlg_responses = []

    for i in range(len(dm_output)):
        tags = nlu_output[i]
        for k, v in dm_output[i].items():
            tags[k] = v
        
        nlg_responses.append(get_nlg_output(tags))
    
    return '\nBOT:  '.join(nlg_responses)


def get_nlg_output(tags):
    if not tags: return fill_template('not_processed.txt')

    if 'list' in tags:
        if tags['list'] == 0: return fill_template('zero_results.txt')

        if 'question' in tags:
            if tags['question'] == 'TO_LIST': return fill_template('list_to_list.txt', tags['list'])
            if tags['question'] == 'HOW_MANY':
                if 'request' in tags and tags['request'] == 'title':
                    if 'actor' in tags and 'genre' in tags: return fill_template('list_actor_genre.txt', tags['list'], tags['actor'], tags['genre'])
                    if 'actor' in tags : return fill_template('list_actor.txt', tags['list'], tags['actor'])
                    if 'genre' in tags: return fill_template('list_genre.txt', tags['list'], tags['genre'])

                return fill_template('list_how_many.txt', tags['list'])

    if 'print' in tags:
        if tags['print'] == 'greeting': return fill_template('greeting.txt')
        if tags['print'] == 'exit': return fill_template('exit.txt')
        if tags['print'] == 'continue': return fill_template('continue.txt')
        if tags['print'] == 'title': return fill_template('print_results.txt', '\n\t'+'\n\t'.join(r[0] for r in tags['results']))
        if tags['print'] == 'director' and 'title' in tags: return fill_template('print_director_title.txt', tags['results'][0][0], tags['title'])
        if tags['print'] == 'actor' and 'title' in tags: return fill_template('print_actor_title.txt', tags['results'][0][0], tags['title'])
        if tags['print'] == 'actor' or tags['print'] == 'director': return fill_template('print_crew.txt', tags['results'][0][0])

    return fill_template('default.txt')


def fill_template(file_name, *args):
    with open(os.path.join(BASE_PATH, file_name)) as f:
        template = random.choice(f.readlines())
        return str.format(template.strip(), *args)
