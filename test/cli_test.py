import unittest

# pydini
from pydini.cli import cli

class TestCliMethods(unittest.TestCase):

    def test_cli(self):
        self.assertTrue(cli("file /Users/bernhardesperester/git/python-scriptable-houdini/examples/example"))
        