import hou
import logging

from json import dumps
from os.path import join, isfile
from importlib import import_module

# pydini

workingDirectory = "/Users/bernhardesperester/git/python-scriptable-houdini/temp"


class BlockCompiledException(Exception):
    """Block Compiled Exception"""


class LineIsCommentException(Exception):
    """Line Is Comment Exception"""


class LineIsEmptyLineException(Exception):
    """Line Is Empty Line Exception"""


class MissingBlockException(Exception):
    """Missing Block Exception"""


def getBlockFile(block):
    return join(workingDirectory, block.hash())


def commandProcessor(moduleName, arguments, chain):
    module = import_module("pydini.blocks.{}".format(moduleName))

    if hasattr(module, "blockFactory"):
        previousBlock = chain[-1] if len(chain) else None
        block = module.blockFactory(arguments, previousBlock)

        blockFile = getBlockFile(block)

        if isfile(blockFile):
            logging.info("Skip existing block: {} {}".format(moduleName, block.hash()))

            chain.append(block)

            raise BlockCompiledException()
        elif previousBlock:
            previousBlockFile = getBlockFile(previousBlock)

            if isfile(previousBlockFile):
                hou.hipFile.load(previousBlockFile)
        
        block.execute()

        hou.hipFile.save(blockFile)

        chain.append(block)

        logging.info("Executed block: {} {}".format(moduleName, block.hash()))

        return True

    raise MissingBlockException(moduleName)


def lineProcessor(line, chain):
    if line.startswith("#"):
        raise LineIsCommentException()

    if not line:
        raise LineIsEmptyLineException()

    arguments = line.split(" ")

    moduleName = arguments[0]
    arguments = arguments[1:]

    return commandProcessor(moduleName, arguments, chain)


def process(path):
    chain = []

    with open(path) as f:
        for line in f:
            line = line.strip()

            try:
                lineProcessor(line, chain)
            except BlockCompiledException:
                pass
            except LineIsCommentException:
                logging.info(line)
            except LineIsEmptyLineException:
                pass


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    process("/Users/bernhardesperester/git/python-scriptable-houdini/examples/example")
    