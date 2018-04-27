import os
basedir = os.path.abspath(os.path.dirname(__file__))

local = 'postgresql:///waristea'
remote = 'postgres://kghlcdgdfomzez:6245b60f804388d8e10ab4f6779fd7697bb4539e695d10ab708c9593eeadd16c@ec2-23-23-180-121.compute-1.amazonaws.com:5432/dihc3t6q16qlj'
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'f:$\x80\xac\xc3\xb6\x07\x84\x8bL\x06\x14\x17\xfe\t\x85^\xa3\xbf)\r\x19V'
    SQLALCHEMY_DATABASE_URI = remote

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
