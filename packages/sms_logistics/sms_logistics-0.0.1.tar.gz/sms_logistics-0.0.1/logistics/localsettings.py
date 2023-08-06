# you should configure your database here before doing any real work.
# see: http://docs.djangoproject.com/en/dev/ref/settings/#databases

# for sqlite3:
#DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": "db.sqlite3",
#        "USER": "",
#        "PASSWORD": "",
#        "HOST": "",
# since we might hit the database from any thread during testing, the
# in-memory sqlite database isn't sufficient. it spawns a separate
# virtual database for each thread, and syncdb is only called for the
# first. this leads to confusing "no such table" errors. We create
# a named temporary instance instead.
#        "TEST_NAME": "test_db.sqlite3",
#    }
#}

# the rapidsms backend configuration is designed to resemble django's
# database configuration, as a nested dict of (name, configuration).
#
# the ENGINE option specifies the module of the backend; the most common
# backend types (for a GSM modem or an SMPP server) are bundled with
# rapidsms, but you may choose to write your own.
#
# all other options are passed to the Backend when it is instantiated,
# to configure it. see the documentation in those modules for a list of
# the valid options for each.
INSTALLED_BACKENDS = {
    #"att": {
    #    "ENGINE": "rapidsms.backends.gsm",
    #    "PORT": "/dev/ttyUSB0"
    #},
    "end2end": {
        "ENGINE": "rapidsms.backends.http",
        "PORT": 8002,
        #"gateway_url" : "http://gw1.promessaging.com/sms.php",
        "gateway_url" : "http://127.0.0.1:8005",
        "params_outgoing": "user=my_username&snr=%2B&password=my_password&id=%(phone_number)s&text=%(message)s",
        "params_incoming": "snr=%(phone_number)s&msg=%(message)s"
    },
    "message_tester": {
        "ENGINE": "rapidsms.backends.bucket",
    },
}

# for postgresql:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "logistics",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
    }
}

TESTING_DATABASES= {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",#
        "NAME": "logistics.sqlite3",
    }
}

DJANGO_LOG_FILE = "logistics.django.log"
LOG_SIZE = 1000000
LOG_LEVEL   = "DEBUG"
LOG_FILE    = "logistics.log"
LOG_FORMAT  = "[%(name)s]: %(message)s"
LOG_BACKUPS = 256 # number of logs to keep
