"""
This module is used to invoke the gRPC todolists.TodoLists.Delete Stub

Examples:
        This module can be executed as a script, this way it will execute the todolists.TodoLists.Delete Stub,
        it expects a positional argument to define the List `id` to delete.
        If no argument is defined it will be requested by user input

            $ python stub_delete_list.py 10

        The module can also be imported to call the `delete_list` function and invoke the .Delete Stub.

            $ from proto_client.stub_delete_list import delete_list
            $ delete_list(10, grpc_channel)

Attributes:
    stub_delete_list.delete_list (function): Function use to invoke the gRPC to delete a TodoList by id
"""
import os
import sys
import grpc
from grpc._channel import _InactiveRpcError, Channel
from grpc import StatusCode

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import proto.v1.todolists_pb2 as todolists_pb2  # pylint: disable=wrong-import-position
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc  # pylint: disable=wrong-import-position
from config.config import GRPC_SERVER_PORT  # pylint: disable=wrong-import-position
from proto_client.helpers import get_input  # pylint: disable=wrong-import-position


def delete_list(list_id: id, channel: Channel) -> todolists_pb2.Empty:
    """
    Invoke the TodoLists.Delete gRPC to delete a List by `id`

    :param list_id: `id` of List to delete
    :param channel: gRPC channel used to invoke the Stub

    :return: Empty

    :raise _InactiveRpcError:
        If the gRPC server is UNAVAILABLE
        If a list with `list_id` do not exist in the DB
    """
    print('Calling TodoLists.Delete with List id "{}"'.format(list_id))
    try:
        stub = todolists_pb2_grpc.TodoListsStub(channel)
        response = stub.Delete(todolists_pb2.DeleteListRequest(id=list_id))
        print('TodoList with id "{}" deleted'.format(list_id))
        return response
    except _InactiveRpcError as ex:
        exception_code = ex.args[0].code  # pylint: disable=no-member
        exception_details = ex.args[0].details  # pylint: disable=no-member
        if exception_code == StatusCode.UNAVAILABLE:
            print('Seems that the gRPC Server is Unavailable. - {}'.format(exception_details))
        elif exception_code == StatusCode.NOT_FOUND:
            print('{}'.format(exception_details))
        else:
            print('Error deleting TodoList - {}'.format(exception_details))
            raise ex


def main():
    """
    Main when executed as script
    :return:
    """
    # List `id` can be specified by positional arguments, if it will be requested as input
    try:
        _list_id = sys.argv[1]
    except IndexError:
        _list_id = int(get_input('Please insert the TodoList `id` to delete: ').strip())
    with grpc.insecure_channel('localhost:{}'.format(GRPC_SERVER_PORT)) as _channel:
        delete_list(int(_list_id), _channel)


if __name__ == '__main__':
    main()
