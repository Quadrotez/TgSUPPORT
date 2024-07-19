import io
import json
import string
import random

from functions import init
from variables import *

from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

db, cursor = init.database()


def add(chat_id: int, content: str, type_problem: str, caption: str = None):

    while True:
        id_appeal = (''.join(random.choice(string.ascii_letters + string.digits) for i in range(
                           default_password_length)))

        if cursor.execute('SELECT * FROM APPEALS WHERE ID = ?', (id_appeal,)).fetchall():
            continue

        break

    cursor.execute('INSERT INTO APPEALS (ID, CHAT_ID, CONTENT, STATUS, TYPE_PROBLEM) VALUES (?, ?, ?, ?, ?)',
                   (id_appeal, chat_id, __generate_content__(content, caption), False, type_problem))
    db.commit()

    return id_appeal


def delete(id_appeal):
    (cursor.execute('DELETE FROM APPEALS WHERE ID = ?', (id_appeal,)), db.commit())


def get_content(id_appeal):
    try:
        return json.loads(cursor.execute('SELECT CONTENT FROM APPEALS WHERE ID = ?', (id_appeal,)).fetchall()[0][0])
    except TypeError:
        return {'type': 'text', 'content': 'None'}


def get_chat_id(id_appeal):
    return cursor.execute('SELECT CHAT_ID FROM APPEALS WHERE ID = ?', (id_appeal,)).fetchall()[0][0]


def get_type_problem(id_appeal):
    return __redo_type_problem__(cursor.execute('SELECT TYPE_PROBLEM FROM APPEALS WHERE ID = ?',
                                                (id_appeal,)).fetchall()[0][0])


def get_appeals():
    return [i[0] for i in cursor.execute('SELECT ID FROM APPEALS').fetchall()]


def __generate_content__(content, caption):
    if type(content) is str:
        return json.dumps({'type': 'text', 'content': content})

    elif type(content) is bytes:
        return json.dumps({'type': 'photo', 'content': str(content), 'caption': caption})


def __redo_type_problem__(type_problem: str):
    type_problem = eval(f'p{type_problem}')

    return type_problem


async def blit_problem(id_appeal, bot: Bot, chat_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=answer, callback_data=f'ANSWER_APPEAL {id_appeal}')
    builder.button(text=delete_appeal, callback_data=f'DELETE_APPEAL {id_appeal}')
    builder.adjust(1, 1)

    if get_content(id_appeal)['type'] == 'text':
        await bot.send_message(chat_id, new_appeal.format(get_chat_id(id_appeal), id_appeal, get_type_problem(id_appeal),
                                                          get_content(id_appeal)['content']),
                               reply_markup=builder.as_markup())

    elif get_content(id_appeal)['type'] == 'photo':
        await bot.send_photo(chat_id, caption=new_appeal.format(get_chat_id(id_appeal), id_appeal, get_type_problem(id_appeal),
                                                          get_content(id_appeal)['caption']),
                             photo=types.BufferedInputFile(eval(get_content(id_appeal)['content']),
                                                           filename='1'), reply_markup=builder.as_markup())
