import json
import string
import random

from functions import init
from variables import *

db, cursor = init.database()


def add(chat_id: int, content: str, type_problem: str):
    id_appeal = (''.join(random.choice(string.ascii_letters + string.digits) for i in range(
                           default_password_length)))

    cursor.execute('INSERT INTO APPEALS (ID, CHAT_ID, CONTENT, STATUS, TYPE_PROBLEM) VALUES (?, ?, ?, ?, ?)',
                   (id_appeal, chat_id, __generate_content__(id_appeal, content), False, type_problem))
    db.commit()

    return id_appeal


def delete(id_appeal):
    (cursor.execute('DELETE FROM APPEALS WHERE ID = ?', (id_appeal,)), db.commit())


def get_content(id_appeal):
    content_dict = json.loads(cursor.execute('SELECT CONTENT FROM APPEALS WHERE ID = ?', (id_appeal,)).fetchall()[0][0])

    if content_dict['type'] == 'text':
        return content_dict['content']


def get_chat_id(id_appeal):
    return cursor.execute('SELECT CHAT_ID FROM APPEALS WHERE ID = ?', (id_appeal,)).fetchall()[0][0]


def get_type_problem(id_appeal):
    return __redo_type_problem__(cursor.execute('SELECT TYPE_PROBLEM FROM APPEALS WHERE ID = ?',
                                                (id_appeal,)).fetchall()[0][0])


def get_appeals():
    return [i[0] for i in cursor.execute('SELECT ID FROM APPEALS').fetchall()]


def __generate_content__(id_appeal, content):
    if type(content) is str:
        return json.dumps({'type': 'text', 'content': content})


def __redo_type_problem__(type_problem: str):
    type_problem = eval(f'p{type_problem}')


    return type_problem
