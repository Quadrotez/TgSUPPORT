from functions import init

db, cursor = init.database()


def set_value(chat_id: int, value_condition: str):
    cursor.execute('UPDATE USERS SET ROLE = ? WHERE CHAT_ID = ?', (value_condition,
                                                                   chat_id))
    db.commit()

    return True


def get(chat_id: int):
    return str(cursor.execute('SELECT ROLE FROM USERS WHERE CHAT_ID = ?',
                              (chat_id,)).fetchall()[0][0])


def get_all(role: str):
    return [i[0] for i in cursor.execute('SELECT CHAT_ID FROM USERS WHERE ROLE = ?', (role,))]
