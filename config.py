import os


class Config:
    # SECRET_KEY=os.environ.get('SECRET_KEY')
    SECRET_KEY = 'tvybuinocdwmls'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:mock@localhost/blogdb'
    DEBUG = True


class ProdConfig(Config):
    uri = os.getenv('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = uri


class TestConfig(Config):
    pass


config_options = {
    "development": DevConfig,
    "production": ProdConfig,
    "test": TestConfig,
}
