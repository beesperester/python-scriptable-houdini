import hou
from argparse import ArgumentParser

# pydini
from pydini.classes.block import Block

class BlockFile(Block):
    
    def parse(self, arguments):
        parser = ArgumentParser("file")

        modules = parser.add_subparsers(dest="module")

        openParser = modules.add_parser("open")
        openParser.add_argument("path")

        saveParser = modules.add_parser("save")
        saveParser.add_argument("path")

        parsedArguments = parser.parse_args(arguments)

        return parsedArguments

    def execute(self):
        if self.parsedArguments.module == "open":
            hou.hipFile.load(self.parsedArguments.path)

        if self.parsedArguments.module == "save":
            hou.hipFile.save(self.parsedArguments.path)

def blockFactory(arguments, previousBlock):
    return BlockFile(arguments, previousBlock)