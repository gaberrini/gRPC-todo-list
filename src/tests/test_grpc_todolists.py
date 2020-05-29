import unittest
from proto_client.create_list_stub import create_list

from tests.base_test_class import BaseTestClass


class TestGrpcTodoLists(BaseTestClass):

    def test_create_list(self):
        create_list('TestList333', self.channel)


if __name__ == '__main__':
    unittest.main()
