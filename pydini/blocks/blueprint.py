import hou
from argparse import ArgumentParser

# pydini
from pydini.classes.block import Block
from pydini.process import process

class BlockBlueprint(Block):
    
    def parse(self, arguments):
        parser = ArgumentParser("file")

        modules = parser.add_subparsers(dest="module")

        fetchParser = modules.add_parser("fetch")
        fetchParser.add_argument("path")

        parsedArguments = parser.parse_args(arguments)

        return parsedArguments

    def execute(self):
        if self.parsedArguments.module == "fetch":
            process(self.parsedArguments.path)

def blockFactory(arguments, previousBlock):
    return BlockBlueprint(arguments, previousBlock)