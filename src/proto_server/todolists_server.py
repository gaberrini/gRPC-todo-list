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
    def create_todo_lists_unique_name_error(list_name: str) -> status_pb2.Status:
        """
        Create a gRPC error status to abort the stub invoke with an error.

        This error will be created when the stub wants to create a List which name already exist in the DB.

        :param list_name: name of list that already exist in the DB
        :return: The status to be used to abort stub invoke with error
        """
        return status_pb2.Status(
            code=code_pb2.INVALID_ARGUMENT,
            message='List name must be unique, list with name "{}" already exist.'.format(list_name),
        )

    @staticmethod
    def create_todo_lists_not_found_error(list_id: str) -> status_pb2.Status:
        """
        Create a gRPC error status for not found resource

        :param list_id: id of list not found in DB
        :return: The status to be used to abort stub invoke with error
        """
        return status_pb2.Status(
            code=code_pb2.NOT_FOUND,
            message='List id "{}" not found.'.format(list_id),
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
            context.abort_with_status(rpc_status.to_status(self.create_todo_lists_unique_name_error(request.name)))

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
            context.abort_with_status(rpc_status.to_status(self.create_todo_lists_not_found_error(request.id)))


def create_server() -> [_Server, int]:
    """
    Create a gRPC Server that handles todolists.TodoLists gRPC Service

    :return: gRPC _Server, defined insecure port listened by the Server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todolists_pb2_grpc.add_TodoListsServicer_to_server(TodoLists(), server)
    port = server.add_insecure_port('[::]:50051')
    return server, port


def serve():
    """
    Create the gRPC Server that handles todolists.TodoLists gRPC Service

    Start it and wait for connections until its termination.

    :return:
    """
    print('Running TodoLists gRCP server')
    server, _ = create_server()
    server.start()
    server.wait_for_termination()
