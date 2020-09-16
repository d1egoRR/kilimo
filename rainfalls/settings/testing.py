import environ

from rainfalls.settings.base import *


env = environ.Env()
env.read_env(os.path.join(BASE_DIR, 'environments', '.testing'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('KILIMO_KEY')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, env('SQLITE_DB')),
    }
}

ALLOWED_HOSTS = ['*', 'localhost']
