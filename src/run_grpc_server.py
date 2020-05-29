"""
Module used to run the gRPC server and wait for stub invokes.

Examples:
        This module can be executed as a script, this way it will run the gRPC server and wait for
        stubs connections listening to an insecure port.

            $ python run_grpc_server.py
"""
import proto_server.todolists_server as todolists_server

if __name__ == '__main__':
    todolists_server.serve()
