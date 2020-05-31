"""Helper functions shared by stubs"""

def get_input(message: str) -> str:
    """
    Get user input, method made to be mocked in tests

    :param message: To show when input is requested
    :return: Input casted to int
    """
    return input(message)
