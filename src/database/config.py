import os


SQL_LITE_DATABASE_PATH = 'sqlite:///{}'.format(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                            '..',
                                                                            'sqlite.db')))

TEST_SQL_LITE_DATABASE_PATH = 'sqlite:///{}'.format(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                                 '..',
                                                                                 'test_sqlite.db')))
