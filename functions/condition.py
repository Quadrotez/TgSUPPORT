import sqlite3
from functions import init

db, cursor = init.database()


def set_value(chat_id: int, value_condition: str):
    cursor.execute('UPDATE USERS SET CONDITION = ? WHERE CHAT_ID = ?', (value_condition,
                                                                        chat_id))
    db.commit()

    return True


def get(chat_id: int):
    return str(cursor.execute('SELECT CONDITION FROM USERS WHERE CHAT_ID = ?',
                              (chat_id,)).fetchall()[0][0])