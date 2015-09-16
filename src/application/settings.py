"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module,
           which should be kept out of version control.

"""
from secret_keys import CSRF_SECRET_KEY, SESSION_KEY
from SecretConfig import SecretConfig


class Config(object):
    # Set secret keys for CSRF protection
    SECRET_KEY = CSRF_SECRET_KEY
    CSRF_SESSION_KEY = SESSION_KEY
    # Flask-Cache settings
    CACHE_TYPE = 'gaememcached'

    TICKET_PRICE = 790

    NOTIFY_EMAIL = "pavel@pavelkral.eu"

    SENDER_EMAIL = "pavel@pavelkral.eu"

    PAYPAL_BUTTON = "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PFWJSNTQVL34U"

    BITCOINPAY_API_PRODUCTION = SecretConfig.BITCOINPAY_API_PRODUCTION

    BITCOINPAY_CALLBACK_PASS = SecretConfig.BITCOINPAY_CALLBACK_PASS

    ADMIN_EMAILS = SecretConfig.ADMIN_EMAILS


class Development(Config):
    DEBUG = True
    CSRF_ENABLED = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    CSRF_ENABLED = True


class Production(Config):
    DEBUG = False
    CSRF_ENABLED = True
