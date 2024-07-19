import asyncio
import io

import aiogram.exceptions
from aiogram import types, Bot, Dispatcher, F
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

    if role.get(message.chat.id) == 'USER':
        if condition.get(message.chat.id) == 'NORMAL':
            builder = InlineKeyboardBuilder()
            builder.button(text=pPRODUCT, callback_data='PROBLEM PRODUCT')
            builder.button(text=pQUESTION_PRODUCT, callback_data='PROBLEM QUESTION_PRODUCT')
            builder.button(text=pCARE_INSTRUCTION, callback_data='PROBLEM CARE_INSTRUCTION')
            builder.button(text=pHOW_SELECT_A_SIZE, callback_data='PROBLEM HOW_SELECT_A_SIZE')
            builder.button(text=pCONNECT_SUPPORT, callback_data='PROBLEM CONNECT_SUPPORT')
            builder.button(text=pCACHEBACK, callback_data='PROBLEM CACHEBACK')

            builder.adjust(*(1 for i in range(1, 6+1)))

            await message.answer(on_start, reply_markup=builder.as_markup())

        elif condition.get(message.chat.id).split(' ')[0] == 'SENDING':
            try:
                await bot.delete_message(message.chat.id, condition.get(message.chat.id).split(' ')[1])
            except aiogram.exceptions.TelegramBadRequest:
                pass

            await message.answer(appeal_was_sent)

            if message.text:
                content = message.text

            elif message.photo:
                photo_bytes = await bot.download_file(
                    (await bot.get_file(message.photo[-1].file_id)).file_path, destination=io.BytesIO())
                photo_bytes.seek(0)
                content = photo_bytes.read()

            else:
                await message.answer('Вы прислали неподдерживаемый тип контента!')
                return

            id_appeal = appeals.add(message.chat.id, content, condition.get(message.chat.id).split(' ')[2],
                                    caption=message.caption if message.caption else None)

            for i in role.get_all('SECURITY'):
                await appeals.blit_problem(id_appeal, bot, i)

            condition.set_value(message.chat.id, 'NORMAL')

    elif role.get(message.chat.id) == 'SECURITY':
        if condition.get(message.chat.id) == 'NORMAL':
            builder = InlineKeyboardBuilder()
            for i in appeals.get_appeals():
                builder.button(text=i, callback_data=f'BLIT_APPEAL {i}')
                builder.adjust(*(i for i in range(1, len(appeals.get_appeals())+1)))

            await message.answer(opened_appeals, reply_markup=builder.as_markup())

        elif condition.get(message.chat.id).split(' ')[0] == 'ANSWER_APPEAL':
            id_appeal = condition.get(message.chat.id).split(' ')[1]
            await bot.send_message(appeals.get_chat_id(id_appeal), answer_skeleton.format(message.text))

            condition.set_value(message.chat.id, 'NORMAL')

            appeals.delete(id_appeal)

            await message.answer(answer_was_sent)


@dp.callback_query()
async def main_callback_query_handler(data: CallbackQuery):
    if data.data.split(' ')[0] == 'PROBLEM':
        builder = InlineKeyboardBuilder()
        builder.button(text=cancel, callback_data='CANCEL_PROBLEM')

        msg = await data.message.answer(on_problem_callback, reply_markup=builder.as_markup())
        condition.set_value(data.message.chat.id, f'SENDING {msg.message_id} {data.data.split(" ")[1]}')

    elif data.data == 'CANCEL_PROBLEM':
        condition.set_value(data.message.chat.id, 'NORMAL')

        await data.message.delete()

        await data.message.answer(canceled)

    elif data.data.split(' ')[0] == 'ANSWER_APPEAL':
        if not cursor.execute('SELECT * FROM APPEALS WHERE ID = ?', (data.data.split(" ")[1],)).fetchall():
            await data.message.answer(appeal_was_closed)
            return

        await data.message.answer(send_your_answer)

        condition.set_value(data.message.chat.id, f'ANSWER_APPEAL {data.data.split(" ")[1]}')

    elif data.data.split(' ')[0] == 'BLIT_APPEAL':
        if not cursor.execute('SELECT * FROM APPEALS WHERE ID = ?', (data.data.split(" ")[1],)).fetchall():
            await data.message.answer(appeal_was_closed)
            return

        await appeals.blit_problem(data.data.split(' ')[1], bot, data.message.chat.id)

    elif data.data.split(' ')[0] == 'DELETE_APPEAL':
        appeals.delete(data.data.split(' ')[1])
        await data.message.answer(appeal_was_deleted)


async def main():
    logging.basicConfig(level=level_logging)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
