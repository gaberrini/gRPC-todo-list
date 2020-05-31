"""
Module with the tests for the gRPC Stubs as scripts

Classes:
    TestStubsTodoLists(BaseTestClass)
"""
import io
import unittest
from unittest.mock import patch, MagicMock

from database.todo_lists_db_handler import TodoListDBHandler
from proto_client.stub_get_lists_paginated import main as main_stub_get_lists_paginated
from proto_client.stub_get_list import main as main_stub_get_list
from proto_client.stub_create_list import main as main_stub_create_list
from proto_client.stub_delete_list import main as main_stub_delete_list
from tests.base_test_class import BaseTestClass


class TestStubsTodoLists(BaseTestClass):
    """
    Test stubs when called as scripts
    """

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('proto_client.stub_get_lists_paginated.get_input')
    def test_stub_get_lists_paginated_script(self, input_mock: MagicMock, print_mock: MagicMock):
        """
        Invoke the get lists paginated stub script

        :param input_mock: Mock to input function
        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        input_mock.return_value = '2'
        [TodoListDBHandler.new_todo_list_entry(str(i)) for i in range(5)]  # pylint: disable=expression-not-assigned

        # When
        main_stub_get_lists_paginated()

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertIn('next_page_number=3', print_mock.getvalue())
        self.assertIn('count=5', print_mock.getvalue())
        self.assertIn('id: {}'.format(db_entries[2].id), print_mock.getvalue())
        self.assertIn('id: {}'.format(db_entries[3].id), print_mock.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('proto_client.stub_get_list.get_input')
    def test_stub_get_list_script(self, input_mock: MagicMock, print_mock: MagicMock):
        """
        Invoke the get lists stub script

        :param input_mock: Mock to input function
        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        test_list_id = TodoListDBHandler.new_todo_list_entry('TestList')
        input_mock.return_value = str(test_list_id)

        # When
        main_stub_get_list()

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertIn('id "{}" and name "{}"'.format(db_entries[0].id, db_entries[0].name), print_mock.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('proto_client.stub_create_list.get_input')
    def test_stub_create_list_script(self, input_mock: MagicMock, print_mock: MagicMock):
        """
        Invoke the create lists stub script

        :param input_mock: Mock to input function
        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        new_list_name = 'TestList'
        input_mock.return_value = new_list_name

        # When
        main_stub_create_list()

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertIn('id "{}" and name "{}"'.format(db_entries[0].id, db_entries[0].name), print_mock.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('proto_client.stub_delete_list.get_input')
    def test_stub_delete_list_script(self, input_mock: MagicMock, print_mock: MagicMock):
        """
        Invoke the delete lists stub script

        :param input_mock: Mock to input function
        :param print_mock: Mock to inspect print calls
        :return:
        """
        # Data
        test_list_id = TodoListDBHandler.new_todo_list_entry('TestList')
        input_mock.return_value = str(test_list_id)

        # When
        main_stub_delete_list()

        # Then
        db_entries = TodoListDBHandler.get_lists_paginated()
        self.assertIn('id "{}" deleted'.format(test_list_id), print_mock.getvalue())
        self.assertEqual(len(db_entries), 0)


if __name__ == '__main__':
    unittest.main()
