from pymysql.cursors import DictCursor

UPDATE_TIME_HOUR = 6
UPDATE_TIME_MIN = 0
UPDATE_TIME_SEC = 0


DATABASE = {
    'host': 'localhost',
    'port': 3306,
    'db': 'asterisk',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}


XML_PATH = '/var/www/html/phonebook.xml'


LOG_PATH = 'phonebook.log'
