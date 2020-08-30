import hou
from argparse import ArgumentParser
from os.path import isfile

# pydini
from pydini.classes.block import Block
from pydini.utilities.hashutilities import hashFile

class BlockHoudini(Block):
    
    def parse(self, arguments):
        parser = ArgumentParser("houdini")

        modules = parser.add_subparsers(dest="module")

        loadParser = modules.add_parser("load")
        loadParser.add_argument("path")

        saveParser = modules.add_parser("save")
        saveParser.add_argument("path")

        parsedArguments = parser.parse_args(arguments)

        if parsedArguments.module == "load" and isfile(parsedArguments.path):
            self.salt = hashFile(parsedArguments.path)

        return parsedArguments

    def execute(self):
        if self.parsedArguments.module == "load":
            hou.hipFile.load(self.parsedArguments.path)

        if self.parsedArguments.module == "save":
            hou.hipFile.save(self.parsedArguments.path)

def blockFactory(arguments, previousBlock):
    return BlockHoudini(arguments, previousBlock)