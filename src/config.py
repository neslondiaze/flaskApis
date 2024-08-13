class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'nedp'
    MYSQL_PASSWORD = 'cielo0'
    MYSQL_DB = 'api_flask'


config = {
    'development': DevelopmentConfig
}