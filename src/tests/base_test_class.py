"""
Base test class used to init test database and test gRPC Server

Classes:
    BaseTestClass(unittest.TestCase)
"""
import unittest
import grpc
import database.config as config
import database.database as db
from proto_server.todolists_server import create_server


class BaseTestClass(unittest.TestCase):
    """
    Attributes:
        grpc_insecure_channel: grpc.Channel used to invoke the gRPC methods from the stubs
        grpc_server: used to execute the gRPC methods

    Database will be dropped and created in setUp
    The gRPC Channel and Server will be created on setUp and restarted on tearDown
    """

    def setUp(self) -> None:
        """
        Set up test environment assigning test DB path, dropping database and then creating it again.
        Create the test grpc_server, and the grpc_insecure_channel to be used to invoke the stubs.
        :return:
        """
        # Set test database path and drop Database, it will be created again when gRPC is created
        config.SQL_LITE_DATABASE_PATH = config.TEST_SQL_LITE_DATABASE_PATH
        db.Database.drop_all()
        db.Database.create_db_tables()
        self.grpc_server, port = create_server()
        self.grpc_server.start()
        self.grpc_insecure_channel = grpc.insecure_channel('localhost:{}'.format(port))

    def tearDown(self) -> None:
        """
        Clean the test environment.
        Drop database, close grpc_insecure_channel and stop the grpc_server
        :return:
        """
        db.Database.drop_all()
        self.grpc_insecure_channel.close()
        self.grpc_server.stop(None)
