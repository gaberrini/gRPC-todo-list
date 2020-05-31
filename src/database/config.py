"""
Database Config variables.

Attributes:
    SQL_LITE_DATABASE_PATH (str): Sql lite database path.
    TEST_SQL_LITE_DATABASE_PATH (str): Sql lite database path used for testing, assigned in the BaseTestClass setUp
    TESTING_ENVIRONMENT (str): Name of testing environment.
    ENVIRONMENT (str): Define the running environment, if it's `TESTING_ENVIRONMENT` Test DB PATH will be assigned
"""
import os

# If its `testing`
TESTING_ENVIRONMENT = 'testing'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

SQL_LITE_DATABASE_PATH = 'sqlite:///{}'.format(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                            '..',
                                                                            'sqlite.db')))

TEST_SQL_LITE_DATABASE_PATH = 'sqlite:///{}'.format(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                                 '..',
                                                                                 'test_sqlite.db')))

SQL_LITE_DATABASE_PATH = TEST_SQL_LITE_DATABASE_PATH if ENVIRONMENT == TESTING_ENVIRONMENT else SQL_LITE_DATABASE_PATH
