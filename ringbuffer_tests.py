#!/usr/bin/env python

import unittest
import ringbuffer

class RingBufferTests (unittest.TestCase):
  def setUp (self):
    self.buffer = ringbuffer.RingBuffer (2)

  def __add_times_number_of_test_strings (self, times):
    for i in range (0, times):
      test_str = 'test%d' %(i+1)
      self.buffer.insert (test_str)

  def test_checking_if_something_is_in_empty_ringbuffer_returns_false (self):
    self.assertFalse (self.buffer.contains ('something'))

  def test_string_test_to_ringbuffer_returns_true_if_we_check_if_it_exists_in_ringbuffer (self):
    self.__add_times_number_of_test_strings (1)
    self.assertTrue (self.buffer.contains ('test1'))

  def test_adding_two_string_we_find_both_when_searching_for_them (self):
    self.__add_times_number_of_test_strings (2)
    self.assertTrue (self.buffer.contains ('test1'))
    self.assertTrue (self.buffer.contains ('test2'))

  def test_adding_test1_and_test2_ringbuffer_does_not_contain_test3 (self):
    self.__add_times_number_of_test_strings (2)
    self.assertFalse (self.buffer.contains ('test3'))

  def test_adding_three_strings_in_ringbuffer_first_elements_is_lost (self):
    self.__add_times_number_of_test_strings (3)
    self.assertFalse (self.buffer.contains ('test1'))

def suite ():
  return unittest.TestLoader().loadTestsFromTestCase (RingBufferTests)

if __name__ == '__main__':
  unittest.TextTestRunner().run (suite ())
