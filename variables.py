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
Id: {0}
Материал обращения: {1}'''
answer = 'Ответить'

