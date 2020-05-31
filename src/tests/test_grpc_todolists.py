"""
Module with the tests for the gRPC Service todolists.TodoLists

Classes:
    TestGrpcTodoLists(BaseTestClass)
"""
import io
import unittest
from unittest.mock import patch, MagicMock

from proto_client.stub_create_list import create_list
from proto_client.stub_get_list import get_list
from proto_client.stub_delete_list import delete_list
from proto_client.stub_get_lists_paginated import get_lists_paginated
from database.todo_lists_db_handler import TodoListDBHandler
from tests.base_test_class import BaseTestClass


class TestGrpcTodoLists(BaseTestClass):
    """
    gRPC Service todolists.TodoLists Tests
    """

    def test_create_lists(self):
        """
        Invoke the create list stub and validate that the list is stored in the database

        :return:
        """
        # Data
        new_list_name = 'TestList'

        # When
        response = create_list(new_list_name, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(len(db_entries), 1, 'Error DB should have only 1 entry')
        self.assertEqual(response.id, db_entries[0].id)
        self.assertEqual(response.name, new_list_name)
        self.assertEqual(response.name, db_entries[0].name)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_list_fail_unique_name(self, print_mock: MagicMock):
        """
        Invoke create list stub should fail when list with that name already exist in the database

        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        test_list_name = 'TestList'
        TodoListDBHandler.new_todo_list_entry(test_list_name)

        # When
        create_list(test_list_name, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(len(db_entries), 1, 'Error DB should have only 1 entry')
        self.assertIn('List name must be unique', print_mock.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_list_fail_server_unavailable(self, print_mock: MagicMock):
        """
        Invoke stub should fail when the server is UNAVAILABLE.

        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        test_list_name = 'TestList'
        self.grpc_server.stop(None)

        # When
        create_list(test_list_name, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(len(db_entries), 0, 'Error DB should have 0 entries')
        self.assertIn('failed to connect to all addresses', print_mock.getvalue())

    def test_get_list(self):
        """
        Invoke the get list stub

        :return:
        """
        # Data
        test_list_id = TodoListDBHandler.new_todo_list_entry('TestList')

        # When
        response = get_list(test_list_id, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(response.id, db_entries[0].id)
        self.assertEqual(response.name, db_entries[0].name)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_list_fail_not_found(self, print_mock: MagicMock):
        """
        Invoke get list stub should fail when list is not found

        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        invalid_id = 666

        # When
        get_list(invalid_id, self.grpc_insecure_channel)

        # Then
        self.assertIn('List with id "{}" not found.'.format(invalid_id), print_mock.getvalue())

    def test_delete_list(self):
        """
        Invoke the delete list stub

        :return:
        """
        # Data
        test_list_id = TodoListDBHandler.new_todo_list_entry('TestList')

        # When
        delete_list(test_list_id, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(len(db_entries), 0)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_list_fail_not_found(self, print_mock: MagicMock):
        """
        Invoke the delete list stub should fail when list does not exist

        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        invalid_id = 666

        # When
        delete_list(invalid_id, self.grpc_insecure_channel)

        # Then
        self.assertIn('List with id "{}" not found.'.format(invalid_id), print_mock.getvalue())

    def test_get_lists_paginated(self):
        """
        Invoke the get lists paginated stub

        :return:
        """
        # Data
        [TodoListDBHandler.new_todo_list_entry(str(i)) for i in range(5)]  # pylint: disable=expression-not-assigned

        # When
        response = get_lists_paginated(2, 2, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(response.next_page_number, '3')
        self.assertEqual(response.count, 5)
        self.assertEqual(len(response.todo_lists), 2)
        self.assertEqual(response.todo_lists[0].id, db_entries[2].id)
        self.assertEqual(response.todo_lists[1].id, db_entries[3].id)

    def test_get_lists_paginated_2(self):
        """
        Invoke the get lists paginated stub

        :return:
        """
        # Data
        [TodoListDBHandler.new_todo_list_entry(str(i)) for i in range(5)]  # pylint: disable=expression-not-assigned

        # When
        response = get_lists_paginated(3, 2, self.grpc_insecure_channel)

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertEqual(response.next_page_number, '')
        self.assertEqual(len(response.todo_lists), 1)
        self.assertEqual(response.todo_lists[0].id, db_entries[4].id)
        self.assertEqual(response.todo_lists[0].id, db_entries[4].id)


if __name__ == '__main__':
    unittest.main()
