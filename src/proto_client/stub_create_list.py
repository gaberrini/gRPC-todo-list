"""
This module is used to invoke the gRPC todolists.TodoLists.Create Stub

Examples:
        This module can be executed as a script, this way it will execute the todolists.TodoLists.Create Stub,
        it accept an optional positional argument to define the new List name. If no argument is defined
        it will try to create a List with the name `TestList`

            $ python stub_create_list.py NewListName

        The module can also be imported to call the `create_list` function and invoke the .Create Stub.

            $ from proto_client.create_list_stub import create_list
            $ create_list('new_list_name', grpc_channel)

Attributes:
    create_list_stub.create_list (function): Function use to invoke the gRPC to create a new TodoList
"""
import os
import sys
import grpc
from grpc._channel import _InactiveRpcError, Channel
from grpc import StatusCode

# Not good practice, add src to python path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import proto.v1.todolists_pb2 as todolists_pb2  # pylint: disable=wrong-import-position
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc  # pylint: disable=wrong-import-position
from config.config import GRPC_SERVER_PORT  # pylint: disable=wrong-import-position


def create_list(name: str, channel: Channel) -> todolists_pb2.CreateListReply:
    """
    Invoke the TodoLists.Create gRPC to create a new List with the defined name

    :param name: name for the new list
    :param channel: gRPC channel used to invoke the Stub

    :return: CreateListReply of invoked stub

    :raise _InactiveRpcError:
        If the gRPC server is UNAVAILABLE
        If a list with that name already exist in the database
    """
    print('Calling TodoLists.Create with name "{}"'.format(name))
    try:
        stub = todolists_pb2_grpc.TodoListsStub(channel)
        response = stub.Create(todolists_pb2.CreateListRequest(name=name))
        print('Created TodoList with id "{}" and name "{}"'.format(response.id, response.name))
        return response
    except _InactiveRpcError as ex:
        exception_code = ex.args[0].code  # pylint: disable=no-member
        exception_details = ex.args[0].details  # pylint: disable=no-member
        if exception_code == StatusCode.UNAVAILABLE:
            print('Seems that the gRPC Server is Unavailable. - {}'.format(exception_details))
        else:
            print('Error creating TodoList - {}'.format(exception_details))
        raise ex


if __name__ == '__main__':
    # New list name can be specified by positional arguments, if not default is used
    try:
        LIST_NAME = sys.argv[1]
    except IndexError:
        LIST_NAME = 'TestList'
    with grpc.insecure_channel('localhost:{}'.format(GRPC_SERVER_PORT)) as _channel:
        create_list(LIST_NAME, _channel)
