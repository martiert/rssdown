#!/usr/bin/env python

import re

class verificator:
  def __init__ (self, accept, reject):
    self._accept = re.compile (accept, re.I)

    if reject:
      self._reject = re.compile (reject, re.I)
      self._has_rejects = True
    else:
      self._has_rejects = False

  def verify (self, title):
    if self._accept.search (title):
      if not self._has_rejects:
        return True
      elif not self._reject.search (title):
        return True
    return False

if __name__ == "__main__":
  verific = verificator ('(revolution)|(supernatural)', '')
  assert (verific.verify ('Revolution 2012 1x2 [HDTV - LOL]'))
  assert (verific.verify ('Supernatural 2012'))
  assert (not verific.verify ('smallwille'))

  verific = verificator ('(revolution)|(supernatural)', '(x264)|(720p)')
  assert (verific.verify ('Revolution 2012 1x2 [HDTV - LOL]'))
  assert (not verific.verify ('Revolution 2012 [x264]'))
  assert (not verific.verify ('Revolution 2012 720p'))

  print "All tests succeeded"
