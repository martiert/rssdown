#!/usr/bin/env python

class RingBuffer:
  def __init__ (self, size=50):
    self.data = [None for i in range (0, size)]
    self.head = 0
    self.size = size

  def insert (self, data):
    self.data[self.head] = data
    self.head = self.head + 1
    if self.head == self.size:
      self.head = 0

  def contains (self, data):
    for test in self.data:
      if test == data:
        return True
    return False
