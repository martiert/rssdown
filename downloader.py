#!/usr/bin/env python

import config_reader
import rssparser
import verificator
import urllib2
import urlparse
import ringbuffer

import os, time, logging

class Downloader:
  def __init__ (self):
    config = self.read_config ()
    self.configs = config.get_map ()
    self.sites = config.get_sites ()
    self.global_config = self.configs['global']
    self.downloads = []
    self.setup_logging ()
    self.already_downloaded = ringbuffer.RingBuffer ()

  def run_main_loop (self):
    timeout = int (self.global_config['scan-wait'])
    self.load_ringbuffer ()

    try:
      while True:
        self.download_new_feeds ()
        time.sleep (timeout)
    except KeyboardInterrupt as interupt:
      print "Interrupted"
      self.save_ringbuffer ()

  def read_config (self):
    configfilename = os.path.join (os.getenv('HOME'), '.rssdown/config.txt')
    file = open (configfilename, 'r')
    config = config_reader.ConfigReader (file)
    file.close ()
    return config

  def load_ringbuffer (self):
    saved_data_name = os.path.join (os.getenv ('HOME'), '.rssdown/downloaded.data')
    if not os.path.exists (saved_data_name):
      return

    writer = open (saved_data_name, 'r')
    for line in writer.readlines ():
      self.already_downloaded.insert (line)
    writer.close ()

  def save_ringbuffer (self):
    saved_data_name = os.path.join (os.getenv ('HOME'), '.rssdown/downloaded.data')
    writer = open (saved_data_name, 'w')

    for data in self.already_downloaded.get_data ():
      if not data == None:
        output = '%s\n' %data
        writer.write (output)
    writer.close ()

  def setup_logging (self):
    logfile = 'downloads.log'
    if self.global_config.has_key('logfile'):
      logfile = self.global_config['logfile']
    logfilename = os.path.join (os.getenv('HOME'), '.rssdown', logfile)

    logging.basicConfig (filename=logfilename, level=logging.INFO)

  def download_new_feeds (self):
    for site in self.sites:
      self.download_links_from_site (self.configs[site])

  def download_links_from_site (self, config):
    (valid_links, valid_titles) = self.get_valid_links (config)
    download_dir = self.get_download_dir (config)

    for i in range (0, len (valid_links)):
      logging.info ('Downloading %s' %valid_links[i])
      self.already_downloaded.insert (valid_titles[i])
      self.download (valid_links[i], download_dir)

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

    return self.get_valid_links_from_valid_titles (titles, links, accept, reject)

  def get_valid_links_from_valid_titles (self, titles, links, accept, reject):
    accepted_links = []
    accepted_titles = []
    verifier = verificator.Verificator (accept, reject)
    for i in range (0, len (titles)):
      if verifier.verify (titles[i]) and not self.already_downloaded.contains (titles[i]):
        accepted_links.append (links[i])
        accepted_titles.append (titles[i])
    return (accepted_links, accepted_titles)
