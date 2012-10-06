#!/usr/bin/env python

class RingBuffer:
  def __init__ (self, size=50):
    self.data = [None for i in range (0, size)]
    self.head = 0
    self.tail = 0
    self.size = size

  def insert (self, data):
    self.move_head ()
    if self.head == self.tail:
      self.tail = self.tail + 1
    self.data[self.head] = data

  def move_head (self):
    self.head = self.head + 1
    if self.head == self.size:
      self.head = 0

  def contains (self, data):
    if self.head > self.tail:
      if self.data_exists_between_tail_and_head (data):
        return True
    else:
      if self.data_exists_between_tail_and_end (data) or self.data_exists_between_zero_and_head (data):
        return True
    return False

  def data_exists_between_tail_and_head (self, data):
    for i in range (self.tail, self.head):
      if self.data[i] == data:
        return True
    return False

  def data_exists_between_tail_and_end (self, data):
    for i in range (self.tail, self.size):
      if self.data[i] == data:
        return True
    return False

  def data_exists_between_zero_and_head (self, data):
    for i in range (0, self.head):
      if self.data[i] == data:
        return True
    return False
