import hou

from json import dumps
from os.path import join, isfile

# pydini
from pydini.block import Block, IsCommentException, IsEmptyLineException

workingDirectory = "/Users/bernhardesperester/git/python-scriptable-houdini/temp"

def getBlockFile(block):
    return join(workingDirectory, block.hash())

def process(path):
    chain = []

    with open(path) as f:
        for line in f:
            line = line.strip()

            try:
                previousBlock = chain[-1] if len(chain) else None
                block = Block(line, previousBlock)
                blockFile = getBlockFile(block)

                if isfile(blockFile):
                    print "Skip existing block: {}".format(block.blockModule.arguments)

                    chain.append(block)

                    continue
                elif previousBlock:
                    previousBlockFile = getBlockFile(previousBlock)

                    if isfile(previousBlockFile):
                        hou.hipFile.load(previousBlockFile)

                block.execute()

                hou.hipFile.save(blockFile)

                chain.append(block)

                print "Executed block: {}".format(block.blockModule.arguments)
            except IsCommentException:
                print line
            except IsEmptyLineException:
                pass