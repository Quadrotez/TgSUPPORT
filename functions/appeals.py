import json
import string
import random

from functions import init
from variables import *

db, cursor = init.database()


def add(chat_id: int, content: str):
    id_appeal = (''.join(random.choice(string.ascii_letters + string.digits) for i in range(
                           default_password_length)))

    cursor.execute('INSERT INTO APPEALS (ID, CHAT_ID, CONTENT, STATUS) VALUES (?, ?, ?, ?)',
                   (id_appeal, chat_id, __generate_content__(id_appeal, content), False))
    db.commit()

    return id_appeal


def get_content(id_appeal):
    content_dict = json.loads(cursor.execute('SELECT CONTENT FROM APPEALS WHERE ID = ?', (id_appeal,)).fetchall()[0][0])

    if content_dict['type'] == 'text':
        return content_dict['content']


def __generate_content__(id_appeal, content):
    if type(content) is str:
        return json.dumps({'type': 'text', 'content': content})
