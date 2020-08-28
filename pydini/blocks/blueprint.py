import hou
from argparse import ArgumentParser
from os.path import isfile

# pydini
from pydini.classes.block import Block
from pydini.process import process
from pydini.utilities.hashutilities import hashFile

class BlockBlueprint(Block):
    
    def parse(self, arguments):
        parser = ArgumentParser("file")

        modules = parser.add_subparsers(dest="module")

        fetchParser = modules.add_parser("fetch")
        fetchParser.add_argument("path")

        parsedArguments = parser.parse_args(arguments)

        if parsedArguments.module == "fetch" and isfile(parsedArguments.path):
            self.salt = hashFile(parsedArguments.path)

        return parsedArguments

    def execute(self):
        if self.parsedArguments.module == "fetch":
            process(self.parsedArguments.path)

def blockFactory(arguments, previousBlock):
    return BlockBlueprint(arguments, previousBlock)