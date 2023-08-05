# legume. Copyright 2009 Dale Reidy. All rights reserved. See LICENSE for details.

import time
import random
import unittest
import legume
from greenbar import GreenBarRunner

class NEventTests(unittest.TestCase):
    def setUp(self):
        self.ne = legume.nevent.Event()
        self.event_raised = False

    def testAddHandler(self):
        def _handler(sender, event): pass
        self.ne += _handler
        self.assertTrue(self.ne.is_handled_by(_handler))

    def testAddHandlerTwiceRaisesError(self):
        def _handler(sender, event): pass
        def addhandler():
            self.ne += _handler

        addhandler()
        self.assertRaises(legume.nevent.NEventError, addhandler)

    def testRemoveHandler(self):
        def _handler(sender, event): pass
        self.ne += _handler
        self.ne -= _handler

        self.assertFalse(self.ne.is_handled_by(_handler))


if __name__ == '__main__':
    mytests = unittest.TestLoader().loadTestsFromTestCase(NEventTests)
    GreenBarRunner(verbosity=2).run(mytests)