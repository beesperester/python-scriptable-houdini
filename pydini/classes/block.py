import logging
from json import dumps

# pydini
from pydini.utilities.hashutilities import hashString

class Block(object):

    def __init__(self, arguments, previousBlock):
        self.arguments = arguments
        self.previousBlock = previousBlock if isinstance(previousBlock, Block) else None
        self.salt = None
        
        self.parsedArguments = self.parse(arguments)

    def parse(self, arguments):
        return None

    def execute(self):
        pass

    def serialize(self):
        return {
            "arguments": dumps(self.arguments),
            "previousBlock": self.previousBlock.hash() if self.previousBlock else None,
            "salt": self.salt
        }

    def id(self):
        return "{arguments}.{previousBlock}.{salt}".format(**self.serialize())

    def hash(self):
        return hashString(self.id())