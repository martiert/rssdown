#!/usr/bin/env python

import config_reader
import unittest

class StubFile:
  def __init__ (self):
    self._dummy_file = [
        "[eztv]",
        "regexTrue = ((revolution)|(supernatural))"]
    self._i = 0

  def readlines (self):
    return ['[global]',
      'sleep-time = 30',
      '[eztv]',
      'link = http://www.ezrss.it/feed',
      '',
      'regex-true = ((chuck)|(dexter)|(supernatural))',
      'directory = /home/martin/.torrents',
      '[torrentz]',
      'link = http://rss.torrentz.it/feed?feed=direct&user=test',
      'regex-true = ((chuck)|(dexter))',
      'directory = /home/martin/.torrents']

class TestConfigReader (unittest.TestCase):
  def read_config (self, filereader):
    self.config = config_reader.ConfigReader (filereader)
    self.configMap = self.config.get_map ()

  def test_global_sleep_time_set (self):
    self.read_config (StubFile ())
    self.assertEqual ('30', self.configMap['global']['sleep-time'])

  def test_site_info (self):
    self.read_config (StubFile ())
    self.assertEqual ('http://www.ezrss.it/feed', self.configMap['eztv']['link'])
    self.assertEqual ('((chuck)|(dexter)|(supernatural))', self.configMap['eztv']['regex-true'])
    self.assertEqual ('http://rss.torrentz.it/feed?feed=direct&user=test', self.configMap['torrentz']['link'])
    self.assertEqual ('((chuck)|(dexter))', self.configMap['torrentz']['regex-true'])

  def test_site_list_has_correct_length (self):
    self.read_config (StubFile ())
    self.assertEqual (2, len (self.config.get_sites ()))

  def test_site_list_contains_correct_headers (self):
    self.read_config (StubFile ())
    headers = self.config.get_sites ()
    self.assertEquals ('eztv', headers[0])
    self.assertEquals ('torrentz', headers[1])

def suite ():
  return unittest.TestLoader().loadTestsFromTestCase (TestConfigReader)

if __name__ == '__main__':
  unittest.TextTestRunner().run (suite ())
