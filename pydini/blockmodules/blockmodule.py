from json import dumps

# pydini
from pydini.utilities.hashutilities import hashString

class BlockModule(object):

    def __init__(self, arguments):
        self.arguments = arguments
        self.salt = None
        
        self.parsedArguments = self.parse(arguments)

    def parse(self, arguments):
        return None

    def execute(self):
        pass

    def serialize(self):
        return {
            "arguments": dumps(self.arguments),
            "salt": self.salt
        }

    def hash(self):
        return hashString("{arguments}.{salt}".format(**self.serialize()))