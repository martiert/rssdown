#!/usr/bin/env python

import re

class ConfigReader:
  def __init__(self, reader):
    self.config = {}
    self.heads = []
    self.last_head = ''
    self.read_all(reader)

  def get_map(self):
    return self.config

  def get_sites(self):
    return self.heads

#private functions
  def read_all(self, reader):
    lines = reader.readlines()
    for line in lines:
      self.add_to_config(line)

  def add_to_config(self, line):
    if self.is_header(line):
      self.add_header(line)
    else:
      self.add_line_as_key_value_pair (line)

  def is_header(self, line):
    result = self.get_header_name(line)
    if result:
      return True
    return False

  def add_header(self, line):
    header = self.get_header_name(line)
    self.add_header_to_config_map(header)
    self.add_header_to_header_array(header)

  def get_header_name(self, line):
    header = re.compile(r'(?<=\[)\w+(?=\])')
    result = header.search(line)
    if result:
      return result.group(0)

  def add_header_to_config_map(self, header):
    self.last_head = header
    self.config[self.last_head] = {}

  def add_header_to_header_array(self, header):
    if header != 'global':
      self.heads.append(header)

  def add_line_as_key_value_pair(self, line):
    if line.strip () == '':
      return
    key, value = self.split_and_strip_line(line)
    self.config[self.last_head][key] = value

  def split_and_strip_line(self, line):
    splitted = line.split(' = ')
    if len(splitted) == 2:
      return (splitted[0].strip(), splitted[1].strip())
