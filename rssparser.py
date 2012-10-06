#!/usr/bin/env python

import feedparser

class RssParser:
  def __init__ (self, rssurl):
    feed = feedparser.parse (rssurl)
    self.items = feed["items"]

  def get_title_link_pairs (self):
    titles = []
    links = []
    for item in self.items:
      titles.append (item['title'])
      links.append (item['link'])

    return (titles, links)

if __name__ == '__main__':
  parser = RssParser ('http://www.ezrss.it/feed')
  pairs = parser.get_title_link_pairs ()

  for pair in pairs:
    print pair
