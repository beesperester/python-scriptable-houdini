from argparse import ArgumentParser

# pydini
from pydini.process import process

def cli(cmd = None):
    parser = ArgumentParser("pydini")
    
    modules = parser.add_subparsers(dest="module")

    fileParser = modules.add_parser("file")
    fileParser.add_argument("path")

    arguments = parser.parse_args(cmd.split(" ")) if cmd else parser.parse_args()

    if arguments.module == "file":
        process(arguments.path)

    return True