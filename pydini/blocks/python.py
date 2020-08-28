from os.path import isfile, dirname, basename, splitext
from argparse import ArgumentParser
from imp import load_source

# pydini
from pydini.classes.block import Block
from pydini.utilities.hashutilities import hashFile


class BlockRun(Block):

    def parse(self, arguments):
        parser = ArgumentParser("python")

        modules = parser.add_subparsers(dest="module")

        fileParser = modules.add_parser("file")
        fileParser.add_argument("path")
        fileParser.add_argument("method", default="main")

        execParser = modules.add_parser("exec")
        execParser.add_argument("cmd", nargs="+")

        parsedArguments = parser.parse_args(arguments)

        if parsedArguments.module == "file" and isfile(parsedArguments.path):
            self.salt = hashFile(parsedArguments.path)

        return parsedArguments

    def executeFile(self):
        path = self.parsedArguments.path

        filename, extension = splitext(basename(path))

        if isfile(path):
            module = load_source(filename, path)

            action = getattr(module, self.parsedArguments.method)

            if callable(action):
                action()

    def executeCmd(self):
        cmd = " ".join(self.parsedArguments.cmd)

        for line in cmd.split("\\n"):
            exec(line)

    def execute(self):
        if self.parsedArguments.module == "file":
            self.executeFile()

        if self.parsedArguments.module == "exec":
            self.executeCmd()


def blockFactory(arguments, previousBlock):
    return BlockRun(arguments, previousBlock)