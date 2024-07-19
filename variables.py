import logging

# Конфиг
config_path = 'config.ini'
encoding = 'UTF-8'

# База данных
db_path = 'db.db'

# Логгинг
level_logging = logging.DEBUG

# Генерация паролей
default_password_length = 20

# Тексты
on_start = 'Выберите тип вашего вопроса:'
on_problem_callback = 'Пришлите ваше сообщение. Поддержка ответит совсем скоро!'
cancel = '❌Отмена'
canceled = 'Вы успешно отменили вашу заявку в службу поддержки!'
you_are_a_security = 'Теперь Вы часть персонала!'
new_appeal = '''Новое обращение!
Chat_Id: #{0}
Id: {1}
Тип обращения: {2}
Материал обращения: {3}'''
answer = 'Ответить'
answer_skeleton = '''Поддержка ответила на ваше обращение:
{0}'''
appeal_was_sent = 'Вы успешно отправили заявку в службу поддержки! Поддержка ответит так скоро, как сможет'
appeal_was_closed = 'Обращение было закрыто!'
answer_was_sent = 'Ответ отправлен!'
send_your_answer = 'Пришлите ваш ответ:'
opened_appeals = 'Открытые, на данный момент, обращения:'
delete_appeal = 'Удалить обращение'
appeal_was_deleted = 'Обращение успешно было удалено!'

# Типы проблем
pPRODUCT = 'Проблема с товаром'
pQUESTION_PRODUCT = 'Вопрос по товару'
pCARE_INSTRUCTION = 'Инструкция по уходу'
pHOW_SELECT_A_SIZE = 'Как правильно подобрать размер?'
pCONNECT_SUPPORT = 'Связаться с поддержкой'
pCACHEBACK = 'Получить кэшбек'
