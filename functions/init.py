import os
import sqlite3
import random
import string
from configparser import ConfigParser
from variables import *


def config():
    (l_config := ConfigParser()).read(config_path)

    if not os.path.exists(config_path) or not l_config.has_section('GENERAL'):
        open(config_path, 'w', encoding=encoding).write('')

        l_config.add_section('GENERAL')
        l_config['GENERAL']['BOT_TOKEN'] = input('Введите токен бота: ')

        security_password = input('Введите пароль персонала (Прочерк для его автоматической генерации): ')
        l_config['GENERAL']['SECURITY_PASSWORD'] = security_password if security_password else str(
            (''.join(random.choice(string.ascii_letters+string.digits) for i in range(default_password_length))))

        l_config.write(open(config_path, 'w', encoding=encoding))

    return l_config


def database():
    db = sqlite3.connect('db.db')

    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (CHAT_ID INT, NAME TEXT, USERNAME TEXT, CONDITION TEXT,
    ROLE TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS APPEALS (ID TEXT PRIMARY KEY, CHAT_ID INT, CONTENT TEXT, 
    STATUS BOOLEAN, TYPE_PROBLEM TEXT)''')

    return db, cursor

