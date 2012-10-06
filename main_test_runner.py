#!/usr/bin/env python

import unittest

import verificator_tests
import config_reader_tests

tests = [verificator_tests.suite (),
        config_reader_tests.suite ()]


if __name__ == '__main__':
  suite = unittest.TestSuite ()
  for test in tests:
    suite.addTests (test)

  unittest.TextTestRunner().run (suite)
