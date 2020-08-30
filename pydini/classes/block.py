import logging
from json import dumps

# pydini
from pydini.utilities.hashutilities import hashString


class Block(object):
    """ Block class. """

    def __init__(self, arguments, previousBlock):
        """ Initialize Block instance.

        Args:
            list[string]                arguments
            pydini.classes.block.Block  previousBlock

        """

        self.arguments = arguments
        self.previousBlock = previousBlock if isinstance(previousBlock, Block) else None
        self.salt = None
        
        self.parsedArguments = self.parse(arguments)

    def parse(self, arguments):
        """ Parse arguments.

        Args:
            list[string]    arguments

        Returns:
            tuple
        """

        return None

    def execute(self):
        pass

    def serialize(self):
        """ Serialize Block.

        Returns:
            dict
        """

        return {
            "arguments": dumps(self.arguments),
            "previousBlock": self.previousBlock.hash() if self.previousBlock else None,
            "salt": self.salt
        }

    def id(self):
        """ Creates Block ID.

        Returns:
            string
        """

        return "{arguments}.{previousBlock}.{salt}".format(**self.serialize())

    def hash(self):
        """ Creates Block Hash.

        Returns:
            string
        """

        return hashString(self.id())