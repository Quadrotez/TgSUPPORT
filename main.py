import asyncio
import logging
import sqlite3

from functions import *

from aiogram import types, Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.callback_query import CallbackQuery

bot, dp = Bot(config['GENERAL']['BOT_TOKEN']), Dispatcher()


@dp.message()
async def main_text(message: types.Message):
    if not cursor.execute('SELECT * FROM USERS WHERE CHAT_ID = ?', (message.chat.id,)).fetchall():
        cursor.execute('INSERT INTO USERS (CHAT_ID, NAME, USERNAME, CONDITION) VALUES (?, ?, ?, ?)',
                       (message.chat.id,
                        '{0}{1}'.format(message.from_user.first_name, (' ' + message.from_user.last_name) if
                                        message.from_user.last_name else ''), message.from_user.username, 'NORMAL'))
        db.commit()

    if condition.get(message.chat.id) == 'NORMAL':
        builder = InlineKeyboardBuilder()
        builder.button(text='Проблема с товаром', callback_data='PROBLEM PRODUCT')
        # builder.button(text=)

        await message.answer(on_start, reply_markup=builder.as_markup())

    elif condition.get(message.chat.id) == 'SENDING':
        pass


@dp.callback_query()
async def main_callback_query_handler(data: CallbackQuery):
    if data.data.split(' ')[0] == 'PROBLEM':
        await data.message.answer('Пришлите ваше сообщение. Поддержка ответит совсем скоро!')
        condition.set_value(data.message.chat.id, 'SENDING')


async def main():
    logging.basicConfig(level=level_logging)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
