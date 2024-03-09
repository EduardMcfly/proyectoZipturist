from os import environ

class Config:
    SECRET_KEY = environ.get('SECRET_KEY', 'B!1w8NAt1T^%kvhUI*S^')

#Conexion con la base de datos etapa de desarrollo
class DevelopmentConfig(Config):
    DEBUG = environ.get('DEBUG', True)
    MYSQL_HOST = environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = environ.get('MYSQL_DB', 'turismoz')
    MYSQL_PORT = int(environ.get('MYSQL_PORT', 3306))
    MYSQL_CONNECT_TIMEOUT = int(environ.get('MYSQL_CONNECT_TIMEOUT', 10))

config = {
    'development': DevelopmentConfig
}
