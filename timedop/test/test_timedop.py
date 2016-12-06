#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test_timedop.py
    Unit tests for timedop.py v. 0.0.1

    -Christopher Welborn 12-05-2016
"""

import sys
import unittest

from .. import timed_call, TimedOp, TimedOut


class TimedCallTests(unittest.TestCase):
    """ Tests for the timed_call function. """
    def test_timed_call_raises(self):
        """ Should raise TimedOut after x seconds. """
        def busy_work(x):
            start = 0
            while start < x:
                start += 1
            return start

        result = None
        with self.assertRaises(TimedOut):
            result = timed_call(
                busy_work,
                args=(100000000000, ),
                timeout=1,
            )
        self.assertIsNone(result, msg='busy_work() should\'ve raised!')

    def test_timed_call_returns(self):
        """ Should return the original functions result. """
        result = timed_call(lambda: 2600)
        self.assertEqual(result, 2600, msg='timed_call\'s result is wrong!')


class TimedOpTests(unittest.TestCase):
    """ Tests for the TimedOp object. """

    def test_timedop_set_format_raises(self):
        """ Should raise ValueError for invalid formats. """
        t = TimedOp()
        for invalidfmt in ('', '{', '{} {}'):
            with self.assertRaises(ValueError):
                t.set_format(invalidfmt)

        for validfmt in ('{}', '{0}', '{:0.2f}', '{:0.2f} seconds'):
            t.set_format(validfmt)
            self.assertEqual(
                validfmt,
                t.default_format,
                msg='Failed to set valid format: {}'.format(validfmt)
            )

    def test_timedop_contextman(self):
        """ Can be used as a context manager. """
        t = None
        with TimedOp() as t:
            pass
        self.assertIsNotNone(t, msg='Context manager failed!')

if __name__ == '__main__':
    sys.exit(unittest.main(argv=sys.argv))
