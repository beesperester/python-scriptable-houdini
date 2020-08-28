import logging
import sys

sys.path.append("/Users/bernhardesperester/git/python-scriptable-houdini")

logging.basicConfig(level=logging.DEBUG)

# pydini
from pydini.cli import cli

cli("file /Users/bernhardesperester/git/python-scriptable-houdini/examples/example")