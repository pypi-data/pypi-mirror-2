#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood All Rights Reserved.

"""Scan the articles in yaml format and gather stats.

"""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import codecs
import glob
import gzip
import optparse
import os
import re
import yaml

OK_SINGLE_CHAR_WORDS = {
  'en': 'Ia',
  'pt': 'aoeé',
}

class FetchArticles:
  def __init__(self, lang):
    self.lang = lang
    pass

  def YieldArticles(self):
    limit = 0
    count = 0
    for fname in glob.glob('articles/%s/**/*.yaml.gz' % self.lang):
      print fname
      count += 1
      try:
        fi = gzip.open(fname, 'r')
        ai = yaml.load(fi)
        fi.close()
        yield ai
      except:
        print 'Failed to load', fname
      if limit and count > limit:
        return


def ToList(adict):
  ret = []
  for key, val in adict.items():
    ret.append((val, key))
  return ret

class Stats:
  def __init__(self, lang):
    self.ngram = [{}, {}, {}]
    self.words = {}
    self.lang = lang

  def ReadStats(self):
    fa = FetchArticles(self.lang)
    for article in fa.YieldArticles():
      for title, sections in article.sections:
        for para in sections:
          self.FeedChars(para)
          self.FeedWords(para, article.page)

  def FeedChars(self, chars):
    prev_chars = []
    max_chars = 3
    for char in chars:
      prev_chars.append(char)
      del prev_chars[:-max_chars]
      for n in range(len(prev_chars)):
        l = ''.join(prev_chars[-n-1:])
        try:
          txt = str(l)
        except:
          txt = l
        if txt not in self.ngram[n]:
          self.ngram[n][txt] = 1
        else:
          self.ngram[n][txt] += 1

  def FeedWords(self, chars, page):
    re_word = re.compile(r'\w+', re.UNICODE)
    for grp in re_word.finditer(chars):
      word = grp.group(0)
      if word not in self.words:
        self.words[word] = [1, page, page]
      else:
        self.words[word][0] += 1
        self.words[word][2] = page

  def DumpAll(self):
    names = [
        'stats/%s-freq-stats.txt' % self.lang,
        'stats/%s-bigram-stats.txt' % self.lang,
        'stats/%s-trigram-stats.txt' % self.lang]
    for n in range(3):
      lst = ToList(self.ngram[n])
      lst.sort(reverse=True)
      fname = names[n]
      print 'Creating %s' % fname
      fo = codecs.open(fname, 'w', 'utf-8')
      for count, key in lst:
        if count == 1:
          break
        if '\n' in key or '\r' in key:
          continue
        fo.write('%s %d\n' % (key, count))
      fo.close()

    fname = 'stats/%s-word-stats.txt' % self.lang
    print 'Creating %s' % fname
    fo = codecs.open(fname, 'w', 'utf-8')
    lst = []
    for key, val in self.words.items():
      if val[1] == val[2]:
        continue  # This word only found in one article
      if val[0] == 1:
        continue  # only saw the word once
      if key.isdigit():
        continue  # only numbers
      if len(key) == 1 and key not in OK_SINGLE_CHAR_WORDS[self.lang]:
        continue  # no single digit words.
      if key.upper() == key and len(key) > 1:
        continue  # Drop acronyms, roman numerals
      lst.append((val[0], key))
    lst.sort(reverse=True)
    for count, key in lst:
      fo.write('%s %d\n' % (key, count))
    fo.close()


  def LoadNGram(self, ncount, fname):
    fi = codecs.open(fname, 'r', 'utf-8')
    text = fi.read()
    for line in text.split('\n'):
      prefix = line[:ncount]
      freq = line[ncount+1:]
      if prefix:
        self.ngram[ncount-1][prefix] = int(freq)

  def WindowChars(self, para, window_size, ignore_chars, chars):
    window = []
    freq = {}
    for ch in para:
      ch = ch.lower()
      window.append(ch)
      if ch not in ignore_chars:
        if ch in freq:
          freq[ch] += 1
        else:
          freq[ch] = 1
      if len(window) > window_size:
        if window[0] in freq:
          freq[window[0]] -= 1
        del window[0]
      if len(window) == window_size and self.HasOnlyChars(freq, chars):
        print ''.join(window)

  def HasOnlyChars(self, freq, chars):
    for char in freq:
      if freq[char] > 0 and char not in chars:
        return False
    return True  

  def LookForArticles(self, bytes, ignore_chars, chars):
    """Find articles that have 'chars'.
    Args:
      bytes: How big a snippet of text we want.
      ignore_chars: Skip these chars as if they didn't exist.
      chars: These chars should exist.
    """
    fa = FetchArticles(self.lang)
    for article in fa.YieldArticles():
      for title, sections in article.sections:
        for para in sections:
          self.WindowChars(para, bytes, ignore_chars, chars)

if __name__ == '__main__':
  import optparse
  parser = optparse.OptionParser()
  parser.add_option('-l', '--lang', dest='lang', default='en',
                    help='Language to read (ex. "en", or "pt")')
  (options, args) = parser.parse_args()
  stats = Stats(options.lang)
  stats.ReadStats()
  stats.DumpAll()
  #stats.LoadNGram(2, 'stats/%s-digram-stats.txt' % options.lang)
  #stats.LoadNGram(3, 'en-trigram-stats.txt')
  #stats.LookForArticles(200, ',.<> /=\[]=-+_()!`@#$$%^&*', ' acsdfgetihjkl;')
