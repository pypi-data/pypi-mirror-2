import os
from sys import stderr

from nose.plugins import Plugin

class Drippy(Plugin):
    """ Check for tempfile leaks in tests / contexts.
    """

    _test_count = None

    def __init__(self):
        super(Drippy, self).__init__()
        self._stack = []

    def startContext(self, context):
        self._stack.append((context.__name__, self._countTempfiles()))

    def stopContext(self, context):
        name, precount = self._stack.pop()
        postcount = self._countTempfiles()
        if postcount != precount:
            stderr.write('\n%s%s -- before: %d, after: %d\n' %
                         (' ' * len(self._stack), name, precount, postcount))

    def beforeTest(self, test):
        self._test_count = self._countTempfiles()

    def afterTest(self, test):
        precount = self._test_count
        del self._test_count
        postcount = self._countTempfiles()
        if postcount != precount:
            stderr.write('\n%s%s -- before: %d, after: %d\n' %
                         (' ' * (len(self._stack) + 1),
                          test, precount, postcount))

    def _countTempfiles(self):
        return len([x for x in os.listdir('/tmp') if x.startswith('tmp')])
