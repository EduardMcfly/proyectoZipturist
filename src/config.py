from decouple import config

class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

#Conexion con la base de datos
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'turismoz'

config={
    'development': DevelopmentConfig
}