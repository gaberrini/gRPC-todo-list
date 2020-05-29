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
        - self.grpc_insecure_channel: grpc.Channel used to execute stubs
        - self.grpc_server: used to execute stubs
        - self.db: Database handler

    Database will be dropped and created in setUpClass
    """

    def setUp(self) -> None:
        # Set test database path and drop Database, it will be created again when gRPC is created
        config.SQL_LITE_DATABASE_PATH = config.TEST_SQL_LITE_DATABASE_PATH
        db.Database.drop_all()
        self.grpc_server, port = create_server()
        self.grpc_server.start()
        self.grpc_insecure_channel = grpc.insecure_channel('localhost:{}'.format(port))

    def tearDown(self) -> None:
        self.grpc_insecure_channel.close()
        self.grpc_server.stop(None)
