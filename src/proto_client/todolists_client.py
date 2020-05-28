"""The Python implementation of the GRPC todolists.TodoLists client."""
import grpc

import proto.v1.todolists_pb2 as todolists_pb2
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc


def create_list(name: str):
    """
    Call to the TodoLists.Create gRPC with the defined name

    :param name: name for the new list
    :return:
    """
    print('Calling TodoLists.Create with name {}'.format(name))
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todolists_pb2_grpc.TodoListsStub(channel)
        response = stub.Create(todolists_pb2.CreateListRequest(name=name))
    print("Create response: " + response.message)
    return response
