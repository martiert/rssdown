#!/usr/bin/env python

import feedparser

class rssparser:
  def __init__ (self, rssurl):
    self._url = rssurl
    self._feed = feedparser.parse (self._url)
    self._items = self._feed["items"]

  def get_title_link_pairs (self):
    pairs = []
    for item in self._items:
      pair = (item['title'], item['link'])
      pairs.append (pair)

    return pairs
