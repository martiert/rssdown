#!/usr/bin/env python

import config_reader
import rssparser
import verificator
import urllib2
import urlparse

import os

class Downloader:
  def __init__ (self):
    config = self.read_config ()
    self.configs = config.get_map ()
    self.sites = config.get_sites ()
    self.global_config = self.configs['global']
    self.downloads = []

  def read_config (self):
    configfilename = os.path.join (os.getenv('HOME'), '.rssdown/config.txt')
    file = open (configfilename, 'r')
    config = config_reader.ConfigReader (file)
    file.close ()
    return config

  def download_new_feeds (self):
    for site in self.sites:
      self.download_links_from_site (self.configs[site])

  def download_links_from_site (self, config):
    valid_links = self.get_valid_links (config)
    download_dir = self.get_download_dir (config)

    for link in valid_links:
      self.download (link, download_dir)

  def get_valid_links (self, config):
    parser = rssparser.RssParser (config['link'])
    (titles, links) = parser.get_title_link_pairs ()
    return self.validate_titles_and_return_their_links (config, titles, links)

  def get_download_dir (self, config):
    download_dir = self.global_config['download-dir']
    if config.has_key ('download-dir'):
      download_dir = config['download-dir']
    return download_dir

  def download (self, link, directory):
    filename = self.make_filename_from_link_and_directory (link, directory)
    urlfile = urllib2.urlopen (link)
    localfile = open (filename, 'w')
    localfile.write (urlfile.read ())
    urlfile.close ()
    localfile.close ()

  def make_filename_from_link_and_directory (self, link, directory):
    filename = urlparse.urlsplit (link)[2].split('/')[-1].split('#')[0].split('?')[0]
    urllib = urllib2.urlopen (link)
    if urllib.info ().has_key('Content-Disposition'):
      filename = urllib.info()['Content-Disposition'].split('filename=')[1]
    urllib.close ()
    return os.path.join (directory, filename)

  def validate_titles_and_return_their_links (self, config, titles, links):
    accept = ''
    reject = ''
    if config.has_key ('regex-true'):
      accept = config['regex-true']
    if config.has_key ('regex-false'):
      reject = config['regex-false']

    accepted_links = self.get_valid_links_from_valid_titles (titles, links, accept, reject)
    return accepted_links

  def get_valid_links_from_valid_titles (self, titles, links, accept, reject):
    accepted_links = []
    verifier = verificator.Verificator (accept, reject)
    for i in range (0, len (titles)):
      if verifier.verify (titles[i]):
        accepted_links.append (links[i])
    return accepted_links
