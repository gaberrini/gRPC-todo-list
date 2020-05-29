import unittest
from grpc._channel import _InactiveRpcError
from grpc import StatusCode

from proto_client.create_list_stub import create_list
from database.todo_lists_db_handler import TodoListDBHandler
from tests.base_test_class import BaseTestClass


class TestGrpcTodoLists(BaseTestClass):

    def test_create_lists(self):
        # Data
        new_list_name = 'TestList'

        # When
        response = create_list(new_list_name, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_all()
        self.assertEqual(len(db_entries), 1, 'Error DB should have only 1 entry')
        self.assertEqual(response.id, db_entries[0].id)
        self.assertEqual(response.name, new_list_name)
        self.assertEqual(response.name, db_entries[0].name)

    def test_create_list_fail_unique_name(self):
        # Data
        test_list_name = 'TestList'
        TodoListDBHandler.new_todo_list_entry(test_list_name)

        # When
        with self.assertRaises(_InactiveRpcError) as ex:
            create_list(test_list_name, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_all()
        self.assertEqual(len(db_entries), 1, 'Error DB should have only 1 entry')
        self.assertEqual(ex.exception.args[0].code, StatusCode.INVALID_ARGUMENT)
        self.assertIn('List name must be unique', ex.exception.args[0].details)

    def test_create_list_fail_server_unavailable(self):
        # Data
        test_list_name = 'TestList'
        self.grpc_server.stop(None)

        # When
        with self.assertRaises(_InactiveRpcError) as ex:
            create_list(test_list_name, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_all()
        self.assertEqual(len(db_entries), 0, 'Error DB should have 0 entries')
        self.assertEqual(ex.exception.args[0].code, StatusCode.UNAVAILABLE)
        self.assertIn('failed to connect to all addresses', ex.exception.args[0].details)


if __name__ == '__main__':
    unittest.main()
