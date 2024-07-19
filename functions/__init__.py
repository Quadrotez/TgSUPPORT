from configparser import ConfigParser
from variables import *
from functions import init, condition, role, appeals

config = init.config()
db, cursor = init.database()