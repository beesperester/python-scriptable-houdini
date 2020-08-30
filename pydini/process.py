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
    """ Get block file path.

    Args:
        pydini.classes.block.Block  block

    Returns:
        string
    """

    return join(workingDirectory, block.hash())


def commandProcessor(moduleName, arguments, chain):
    """ Process command.

    Create new Block instance from module name, arguments and previous Block.
    Check if a cooked version of Block exists on filesystem.

    Args:
        string                              moduleName
        list[string]                        arguments
        list[pydini.classes.block.Block]    chain
    
    Returns:
        boolean

    Raises:
        pydini.process.BlockCompiledException
        pydini.process.MissingBlockException
    """

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
    """ Process line.

    Args:
        string                              line
        list[pydini.classes.block.Block]    chain

    Returns:
        boolean

    Raises:
        pydini.process.LineIsCommentException
        pydini.process.LineIsEmptyLineException
    """

    if line.startswith("#"):
        raise LineIsCommentException()

    if not line:
        raise LineIsEmptyLineException()

    arguments = line.split(" ")

    moduleName = arguments[0]
    arguments = arguments[1:]

    return commandProcessor(moduleName, arguments, chain)


def process(path):
    """ Process Blueprint.

    Args:
        string path
    """

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
    