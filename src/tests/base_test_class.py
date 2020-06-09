"""
Base test class used to init test database and test gRPC Server

Classes:
    BaseTestClass(unittest.TestCase)
"""
import unittest
import grpc
import database.database as db
from proto_server.todolists_server import create_secured_server
from proto_client.helpers import create_secured_client_channel
from config.config import GRPC_SERVER_PORT


class BaseTestClass(unittest.TestCase):
    """
    Attributes:
        grpc_secured_channel: grpc.Channel used to invoke the gRPC methods from the stubs
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
        # Drop Database, and create it again
        db.Database.drop_all()
        db.Database.create_db_tables()
        self.grpc_server = create_secured_server(GRPC_SERVER_PORT)
        self.grpc_server.start()
        with create_secured_client_channel('localhost:{}'.format(GRPC_SERVER_PORT)) as _channel:
            self.grpc_secured_channel = _channel

    def tearDown(self) -> None:
        """
        Clean the test environment.
        Drop database, close grpc_insecure_channel and stop the grpc_server
        :return:
        """
        db.Database.drop_all()
        self.grpc_secured_channel.close()
        self.grpc_server.stop(None)
