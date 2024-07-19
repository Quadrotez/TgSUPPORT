import asyncio

from aiogram import types, Bot, Dispatcher
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from functions import *

bot, dp = Bot(config['GENERAL']['BOT_TOKEN']), Dispatcher()


@dp.message()
async def main_text(message: types.Message):
    if not cursor.execute('SELECT * FROM USERS WHERE CHAT_ID = ?', (message.chat.id,)).fetchall():
        cursor.execute('INSERT INTO USERS (CHAT_ID, NAME, USERNAME, CONDITION, ROLE) VALUES (?, ?, ?, ?, ?)',
                       (message.chat.id,
                        '{0}{1}'.format(message.from_user.first_name, (' ' + message.from_user.last_name) if
                                        message.from_user.last_name else ''), message.from_user.username, 'NORMAL',
                        'USER'))
        db.commit()

    if message.text == config['GENERAL']['SECURITY_PASSWORD']:
        role.set_value(message.chat.id, 'SECURITY')
        await message.answer(you_are_a_security)

    elif condition.get(message.chat.id) == 'NORMAL':
        if role.get(message.chat.id) == 'USER':
            builder = InlineKeyboardBuilder()
            builder.button(text='Проблема с товаром', callback_data='PROBLEM PRODUCT')
            # builder.button(text=)

            await message.answer(on_start, reply_markup=builder.as_markup())

    elif condition.get(message.chat.id).split(' ')[0] == 'SENDING':
        await bot.delete_message(message.chat.id, condition.get(message.chat.id).split(' ')[1])

        id_appeal = appeals.add(message.chat.id, message.text)

        builder = InlineKeyboardBuilder()
        builder.button(text=answer, callback_data=f'ANSWER_APPEAL {id_appeal}')

        for i in role.get_all('SECURITY'):
            await bot.send_message(i, new_appeal.format(id_appeal, appeals.get_content(id_appeal)),
                                   reply_markup=builder.as_markup())


@dp.callback_query()
async def main_callback_query_handler(data: CallbackQuery):
    if data.data.split(' ')[0] == 'PROBLEM':
        builder = InlineKeyboardBuilder()
        builder.button(text=cancel, callback_data='CANCEL_PROBLEM')

        msg = await data.message.answer(on_problem_callback, reply_markup=builder.as_markup())
        condition.set_value(data.message.chat.id, f'SENDING {msg.message_id}')

    elif data.data == 'CANCEL_PROBLEM':
        condition.set_value(data.message.chat.id, 'NORMAL')

        await data.message.delete()

        await data.message.answer(canceled)


async def main():
    logging.basicConfig(level=level_logging)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
