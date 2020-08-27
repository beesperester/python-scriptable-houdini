import argparse

def StringToBool(value):
    if isinstance(value, bool):
        return value

    if value.lower() in ["yes", "true", "y", "1"]:
        return True

    if value.lower() in ["no", "false", "n", "0"]:
        return False

    raise argparse.ArgumentTypeError("Boolean value excpected")