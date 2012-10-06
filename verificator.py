#!/usr/bin/env python

import re

class Verificator:
  def __init__ (self, accept, reject):
    self.add_accepts (accept)
    self.add_rejects (reject)

  def verify (self, title):
    if not self.do_accept_title (title):
      return False
    if self.do_reject_title (title):
      return False

    return True

  def do_accept_title (self, title):
    if self.has_accepts and self.accept.search (title):
      return True
    return False

  def do_reject_title (self, title):
    if self.has_rejects and self.reject.search (title):
      return True
    return False

  def add_accepts (self, accepts):
    if accepts:
      self.accept = re.compile (accepts, re.I)
      self.has_accepts = True
    else:
      self.has_accepts = False

  def add_rejects (self, rejects):
    if rejects:
      self.reject = re.compile (rejects, re.I)
      self.has_rejects = True
    else:
      self.has_rejects = False

