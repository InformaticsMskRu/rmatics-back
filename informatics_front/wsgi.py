import os

from informatics_front import create_app

# avialable cofig modules
DEV_CONFIG_MODULE = 'informatics_front.config.DevConfig'
TEST_CONFIG_MODULE = 'informatics_front.config.TestConfig'
PROD_CONFIG_MODULE = 'informatics_front.config.ProdConfig'

# env-config mapping
CONFIG_ENV_MODULES = {
    'development': DEV_CONFIG_MODULE,
    'testing': TEST_CONFIG_MODULE,
    'production': PROD_CONFIG_MODULE,
}

# select appropriate config class based on provided env var
ENV = os.getenv('FLASK_ENV', 'development')
application = create_app(CONFIG_ENV_MODULES.get(ENV, DEV_CONFIG_MODULE))

if __name__ == '__main__':
    application.run()
