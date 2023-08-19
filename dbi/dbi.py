import sqlite3
import time


con = sqlite3.connect('./data/imdb-new.db')
cur = con.cursor()


def execute_general_query(tags):
    query = build_general_query(tags)
    return cur.execute(query).fetchall()
    return []


def build_general_query(tags):
    query = 'SELECT '
    query += ', '.join(get_select_items(tags))
    query += ' FROM basics b'
    query += get_join_statement(tags)
    query += get_where_statement(tags)
    query += get_order_statement(tags)
    query += get_limit_statement(tags)

    print(query)
    return query


def get_select_items(tags):
    items = set()

    if 'request' in tags:
        request = tags['request']
        request_dict = {
            'title': 'b.primaryTitle',
            'year': 'b.startYear',
            'director': 'n.primaryName',
            'actor': 'n.primaryName',
            'birth': 'n.birthYear',
            'death': 'n.deathYear',
        }
        items.add(request_dict[request])

    return items


def get_join_statement(tags):
    statements = []
    values = set(tags.values())

    principal_tags = {
        'character',
        'job',
        'role',
        'category',

        #  name_tags
        'director',
        'actor',
        'birth',
        'death',
    }
    if (values & principal_tags) or (set(tags) & principal_tags):
        statements.append('JOIN principals p ON p.tconst = b.tconst')

    name_tags = {
        'director',
        'actor',
        'birth',
        'death',
    }
    if (values & name_tags) or (set(tags) & name_tags):
        statements.append('JOIN name n ON n.nconst = p.nconst')
    
    rating_tags = {
        'popular',
        'rating',
        'votes',
    }
    if values & rating_tags:
        statements.append('JOIN rating r ON r.tconst = b.tconst')
    
    if any(statements):
        return '\n' + '\n'.join(statements)
    return ''


def get_where_statement(tags):
    filters = []

    if 'title' in tags:
        filters.append(f"b.primaryTitle = '{tags['title']}'")
    
    if 'genre' in tags:
        filters.append(f"b.genres LIKE '%{tags['genre']}%'")
    
    principal_tags = (
        'self',
        'director',
        'cinematographer',
        'composer',
        'producer',
        'editor',
        'actor',
        'actress',
        'writer',
        'production_designer',
        'archive_footage',
        'archive_sound',
    )

    for principal in principal_tags:
        if principal in tags:
            filters.append(f"n.primaryName = '{tags[principal]}'")

    for category in principal_tags:
        if tags.get('request') == category or category in tags:
            filters.append(f"p.category = '{category}'")

    if not any(filters):
        return ''
    return '\nWHERE ' + '\nAND '.join(filters)


def get_order_statement(tags):
    order = tags.get('order')

    if order is None: return ''
    
    order_dict = {
    'new': 'b.startYear DESC',
    'old': 'b.startYear',
    'short': 'b.runtimeMinutes',
    'long': 'b.runtimeMinutes DESC',
    
    'popular': 'r.numVotes DESC',
    'unknown': 'r.numVotes',
    'rate': 'r.averageRating DESC',
    'bad': 'r.averageRating',
    }

    if not order in order_dict:
        return ''

    return f'\nORDER BY {order_dict[order]}'



def get_limit_statement(tags):
    if 'count' in tags:
        return f"\nLIMIT {tags['count']}"
    if 'limit' in tags:
        return f"\nLIMIT {tags['limit']}"
    return ''