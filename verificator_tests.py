#!/usr/bin/env python

import verificator
import unittest

class TestVerificator (unittest.TestCase):
  def test_only_accept_one (self):
    verific = verificator.Verificator ('revolution', '')
    self.assertTrue (verific.verify ('Revolution 2012 1x2 [HDTV - LOL]'))
    self.assertFalse (verific.verify ('smallville'))

  def test_accept_two (self):
    verific = verificator.Verificator ('(revolution)|(supernatural)', '')
    self.assertTrue (verific.verify ('Revolution 2012 1x2 [HDTV - LOL]'))
    self.assertTrue (verific.verify ('Supernatural 2012'))
    self.assertFalse (verific.verify ('smallville'))

  def test_reject_x264_and_720p (self):
    verific = verificator.Verificator ('(revolution)|(supernatural)', '(x264)|(720p)')
    self.assertTrue (verific.verify ('Revolution 2012 1x2 [HDTV - LOL]'))
    self.assertFalse (verific.verify ('Revolution 2012 [x264]'))
    self.assertFalse (verific.verify ('Revolution 2012 720p'))

  def test_empty_accept_and_reject (self):
    verific = verificator.Verificator ('', '')
    self.assertFalse (verific.verify ('Revolution 2012 1x2 [HDTV - LOL]'))
    self.assertFalse (verific.verify ('Revolution 2012 [x264]'))
    self.assertFalse (verific.verify ('Revolution 2012 720p'))

def suite ():
  return unittest.TestLoader().loadTestsFromTestCase (TestVerificator)

if __name__ == '__main__':
  unittest.TextTestRunner().run (suite ())
