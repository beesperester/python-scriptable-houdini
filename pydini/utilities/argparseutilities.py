import argparse

def stringToBool(value):
    """ String to bool.

    Args:
        string  value

    Returns:
        boolean

    Raises:
        argparse.ArgumentTypeError
    """

    if isinstance(value, bool):
        return value

    if value.lower() in ["yes", "true", "y", "1"]:
        return True

    if value.lower() in ["no", "false", "n", "0"]:
        return False

    raise argparse.ArgumentTypeError("Boolean value excpected")