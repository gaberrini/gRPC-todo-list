"""
Base test class used to init test database and test gRPC Server
"""
import unittest
import grpc
import database.config as config
import database.database as db
from proto_server.todolists_server import create_server


class BaseTestClass(unittest.TestCase):
    """
    Add to TestClasses context:
        - self.

    Database will be dropped and created in setUpClass
    """

    def setUp(self) -> None:
        print('Setup test class')

        # Set test database path and drop Database, it will be created again when gRPC is created
        config.SQL_LITE_DATABASE_PATH = config.TEST_SQL_LITE_DATABASE_PATH
        db.Database().drop_all()

        self._server, port = create_server()
        self._server.start()
        self.channel = grpc.insecure_channel('localhost:{}'.format(port))

    def tearDown(self) -> None:
        print('TearDown test class')
        self.channel.close()
        self._server.stop(None)
