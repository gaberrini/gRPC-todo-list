"""The Python implementation of the GRPC todolists.TodoLists server."""
from concurrent import futures
import grpc

import proto.v1.todolists_pb2 as todolists_pb2
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc


class TodoLists(todolists_pb2_grpc.TodoListsServicer):
    pass


def serve():
    print('Running TodoLists gRCP server')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todolists_pb2_grpc.add_TodoListsServicer_to_server(TodoLists(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
