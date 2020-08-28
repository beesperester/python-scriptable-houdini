from os.path import isfile
from argparse import ArgumentParser
from imp import load_source

# pydini
from pydini.classes.block import Block
from pydini.utilities.hashutilities import hashFile

class BlockRun(Block):

    def parse(self, arguments):
        parser = ArgumentParser("run")

        parser.add_argument("moduleName")
        parser.add_argument("path")
        parser.add_argument("method", default="main")

        parsedArguments = parser.parse_args(arguments)

        if isfile(parsedArguments.path):
            self.salt = hashFile(parsedArguments.path)

        return parsedArguments

    def execute(self):
        if isfile(self.parsedArguments.path):
            module = load_source(self.parsedArguments.moduleName, self.parsedArguments.path)

            action = getattr(module, self.parsedArguments.method)

            if callable(action):
                action()

def blockFactory(arguments, previousBlock):
    return BlockRun(arguments, previousBlock)