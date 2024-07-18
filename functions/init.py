import os
import sqlite3
from configparser import ConfigParser
from variables import *


def config():
    (l_config := ConfigParser()).read(config_path)

    if not os.path.exists(config_path):
        open(config_path, 'w', encoding=encoding).write('')

        l_config.add_section('GENERAL')
        l_config['GENERAL']['BOT_TOKEN'] = input('Введите токен бота: ')

        l_config.write(open(config_path, 'w', encoding=encoding))

    return l_config


def database():
    db = sqlite3.connect('db.db')

    cursor = db.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS USERS (CHAT_ID INT, NAME TEXT, USERNAME TEXT, CONDITION TEXT)')

    return db, cursor

