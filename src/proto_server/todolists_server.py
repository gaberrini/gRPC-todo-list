"""
Module with Implementation of the gRPC todolists.TodoLists Service.

Examples:
        This module provides the function to start the gRPC Server for the todolists.TodoLists Service.

            $ import proto_server.todolists_server as todolists_server
            $ todolists_server.serve()

Classes:
    TodoLists(todolists_pb2_grpc.TodoListsServicer): Definition of the gRPC Servicer methods

Attributes:
    todolists_server.create_server (function): Create the gRPC server and add an insecured port to listen to
    todolists_server.serve (function): Run the gRPC server and wait for stubs connections
"""
from concurrent import futures
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from grpc_status import rpc_status
from grpc._server import _Context, _Server
from google.rpc import code_pb2, status_pb2
import grpc

from config.config import MAX_PAGE_SIZE
from database.database import Database
from database.todo_lists_db_handler import TodoListDBHandler
import proto.v1.todolists_pb2 as todolists_pb2
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc


class TodoLists(todolists_pb2_grpc.TodoListsServicer):
    """
    Implementation of gRPC methods for todolists.TodoLists service
    """

    def __init__(self):
        """
        Constructor of TodoLists gRPC service, when executed create the database tables that the Service will use,
        if were not already created.
        """
        Database.create_db_tables()

    @staticmethod
    def create_grpc_error_status(message: str, error_code: int) -> status_pb2.Status:
        """
        Create a gRPC error status

        :param message: Description of the error
        :param error_code: Int that represent the error, codes from code_pb2 module
        :return: Created error status
        """
        return status_pb2.Status(
            code=error_code,
            message=message,
        )

    def Create(self,
               request: todolists_pb2.CreateListRequest,
               context: _Context) -> todolists_pb2.CreateListReply:
        """
        Create New TodoList gRPC method.
        The request will contain a todolist.CreateListRequest

        In the field request.name will be the name of the list that the client wants to create.

        If a list with that `name` already exists in the DB the gRPC will finish with an error code for INVALID_ARGUMENT

        :param request: Request send by the client
        :param context: grpc _Context
        :return: CreateListReply
        """
        try:
            print('Creating TodoList with name "{}"'.format(request.name))
            # Insert a new entry in the TodoList table
            new_entry_id = TodoListDBHandler.new_todo_list_entry(name=request.name)
            print('TodoList created with id "{}"'.format(new_entry_id))
            return todolists_pb2.CreateListReply(id=new_entry_id, name=request.name)
        except IntegrityError:
            context.abort_with_status(rpc_status.to_status(self.create_grpc_error_status(
                'List name must be unique, list with name "{}" already exist.'.format(request.name),
                code_pb2.INVALID_ARGUMENT
            )))

    def Get(self, request: todolists_pb2.GetListRequest, context: _Context) -> todolists_pb2.TodoList:
        """
        Get a TodoList gRPC method.
        The request will contain a todolist.GetListRequest

        In the field request.id will be the id of the list that the client wants to fetch.

        If a list with that `id` do not exist the gRPC will finish with an error code for NOT_FOUND

        :param request: Request send by the client
        :param context: grpc _Context
        :return: TodoList
        """
        try:
            print('Get TodoList with id "{}"'.format(request.id))
            todo_list = TodoListDBHandler.get_todo_list(list_id=request.id)
            return todolists_pb2.TodoList(id=todo_list.id, name=todo_list.name)
        except NoResultFound:
            context.abort_with_status(rpc_status.to_status(self.create_grpc_error_status(
                'List with id "{}" not found.'.format(request.id),
                code_pb2.NOT_FOUND
            )))

    def Delete(self, request: todolists_pb2.DeleteListRequest, context: _Context) -> todolists_pb2.Empty:
        """
        Delete a TodoList gRPC method.
        The request will contain a todolist.DeleteListRequest

        In the field request.id will be the id of the list to delete.

        If a list with that `id` do not exist the gRPC will finish with an error code for NOT_FOUND

        :param request: Request send by the client
        :param context: grpc _Context
        :return: Empty
        """
        try:
            print('Delete TodoList with id "{}"'.format(request.id))
            TodoListDBHandler.delete_todo_list(list_id=request.id)
            return todolists_pb2.Empty()
        except NoResultFound:
            context.abort_with_status(rpc_status.to_status(self.create_grpc_error_status(
                'List with id "{}" not found.'.format(request.id),
                code_pb2.NOT_FOUND
            )))

    def List(self, request: todolists_pb2.ListTodoListsRequest, context: _Context) -> todolists_pb2.ListTodoListsReply:
        """
        List TodoLists gRPC method.

        In the field `request.page_size` the client can define how many lists will be retrieved per page.
            If `page_size` is 0, default value will be 10.
            The maximum value allowed is MAX_PAGE_SIZE, if `page_size` is a bigger value it will be set the max value

        If the field `request.page_number` the client define the desired page number.
            If `page_number` is lower than 1, it will be set to the first page, 1.

        :param request: Send by the client
        :param context: gRPC _Context
        :return:
        """
        raise NotImplementedError()


def create_server(server_port: int) -> [_Server, int]:
    """
    Create a gRPC Server that handles todolists.TodoLists gRPC Service

    :param server_port: Port to listen to
    :return: gRPC _Server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todolists_pb2_grpc.add_TodoListsServicer_to_server(TodoLists(), server)
    server.add_insecure_port('[::]:{}'.format(server_port))
    return server


def serve(server_port: int):
    """
    Create the gRPC Server that handles todolists.TodoLists gRPC Service

    Start it and wait for connections until its termination.

    :param server_port: Port to listen to
    :return:
    """
    print('Running TodoLists gRCP server')
    server = create_server(server_port)
    server.start()
    server.wait_for_termination()
