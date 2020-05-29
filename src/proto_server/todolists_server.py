"""The Python implementation of the GRPC todolists.TodoLists server."""
from concurrent import futures
from grpc_status import rpc_status
from google.rpc import code_pb2, status_pb2
from sqlalchemy.exc import IntegrityError
import grpc

from database.database import Database
from database.todo_lists_db_handler import TodoListDBHandler
import proto.v1.todolists_pb2 as todolists_pb2
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc


class TodoLists(todolists_pb2_grpc.TodoListsServicer):

    def __init__(self):
        Database.create_db_tables()

    @staticmethod
    def create_todo_lists_unique_name_error(name):
        return status_pb2.Status(
            code=code_pb2.INVALID_ARGUMENT,
            message='List name must be unique, list with name "{}" already exist.'.format(name),
        )

    def Create(self, request, context):
        try:
            print('Creating TodoList with name "{}"'.format(request.name))
            # Insert a new entry in the TodoList table
            new_entry_id = TodoListDBHandler.new_todo_list_entry(name=request.name)
            print('TodoList created with id "{}"'.format(new_entry_id))
            return todolists_pb2.CreateListReply(id=new_entry_id, name=request.name)
        except IntegrityError:
            context.abort_with_status(rpc_status.to_status(self.create_todo_lists_unique_name_error(request.name)))
        except Exception as e:
            print('Error in TodoLists.Create gRPC - {}'.format(e))
            raise e


def create_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todolists_pb2_grpc.add_TodoListsServicer_to_server(TodoLists(), server)
    port = server.add_insecure_port('[::]:50051')
    return server, port


def serve():
    print('Running TodoLists gRCP server')
    server, _ = create_server()
    server.start()
    server.wait_for_termination()
