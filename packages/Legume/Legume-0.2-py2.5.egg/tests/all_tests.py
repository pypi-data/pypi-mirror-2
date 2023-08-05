# legume. Copyright 2009 Dale Reidy. All rights reserved. See LICENSE for details.

import unittest
from greenbar import GreenBarRunner
import test_udp
import test_keepalive
import test_events
import test_nevent
import test_newmsg
import test_pingsampler
import test_latency

if __name__ == '__main__':
    suite_udp = unittest.TestLoader().loadTestsFromModule(test_udp)
    suite_keepalive = unittest.TestLoader().loadTestsFromModule(test_keepalive)
    suite_events = unittest.TestLoader().loadTestsFromModule(test_events)
    suite_nevent = unittest.TestLoader().loadTestsFromModule(test_nevent)
    suite_pingsampler = unittest.TestLoader().loadTestsFromModule(test_pingsampler)
    suite_newmsg = unittest.TestLoader().loadTestsFromModule(test_newmsg)
    suite_latency = unittest.TestLoader().loadTestsFromModule(test_latency)

    all_suites = unittest.TestSuite()
    all_suites.addTests([
        suite_udp, suite_keepalive, suite_events,
        suite_nevent, suite_pingsampler, suite_newmsg,
        suite_latency
    ])
    GreenBarRunner(verbosity=2).run(all_suites)