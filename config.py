from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='sqlite:///your_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    # Для настроек почты
    MAIL_USERNAME = config('MAIL_USERNAME', default='your_email@example.com')
    MAIL_PASSWORD = config('MAIL_PASSWORD', default='your_email_password')
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
