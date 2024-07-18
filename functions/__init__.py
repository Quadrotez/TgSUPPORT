from configparser import ConfigParser
from variables import *
from functions import init, condition

config = init.config()
db, cursor = init.database()