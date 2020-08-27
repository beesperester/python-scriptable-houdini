from json import dumps
from importlib import import_module

# pydini
from pydini.utilities.hashutilities import hashString

class IsCommentException(Exception):
    """Is Comment Exception"""

class IsEmptyLineException(Exception):
    """Is Empty Line Exception"""

class Block(object):

    def __init__(self, command, previousBlock):
        if command.startswith("#"):
            raise IsCommentException()

        if not command:
            raise IsEmptyLineException()

        self.previousBlock = previousBlock
        self.blockModule = None

        moduleName = command.split(" ")[0]
        arguments = command.split(" ")[1:]

        module = import_module("pydini.blockmodules.{}".format(moduleName))

        if hasattr(module, "blockModuleFactory"):
            self.blockModule = module.blockModuleFactory(arguments)

    def serialize(self):
        return {
            "hash": self.blockModule.hash() if self.blockModule else None,
            "salt": self.previousBlock.hash() if self.previousBlock else None
        }

    def hash(self):
        return hashString("{hash}.{salt}".format(**self.serialize()))

    def execute(self):
        if self.blockModule:
            self.blockModule.execute()