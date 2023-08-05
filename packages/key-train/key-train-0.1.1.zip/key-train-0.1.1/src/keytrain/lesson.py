#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""Code to load in a lesson plan for use.

I'm using the scan codes because it's more important the positions than the keys.
"""

import codecs
import gettext
import gzip
import logging
import os
import re
import random
import yaml

STATS = {}

class Lesson:
  """Lesson class.  Holds the text and rules for one lesson."""
  def __init__(
      self, us_kbd, to_kbd,
      lang='en', instructions='', preamble='', postamble='',
      strings={},
      allow_errs=True,
      ignore_accent=False,
      ignore_case=False,
      ignore_whitespace=False,
      space_is_return=True,
      use_wikipedia=False,
      new_keys=[], old_keys=[], text='',
      debug=False):
    self.pathname = os.path.dirname(__file__)
    self.us_kbd = us_kbd
    self.to_kbd = to_kbd
    self.time_limit = 60
    self.strings = {}
    for key, string in strings.items():
      self.strings[key] = _(string)
    self.cur_article = None
    self.lang = lang
    self.debug = debug

    self.instructions = instructions
    self.preamble = preamble
    self.postamble = postamble

    self.allow_errs = allow_errs
    self.ignore_accent = ignore_accent
    self.ignore_case = ignore_case
    self.ignore_whitespace = ignore_whitespace
    self.space_is_return = space_is_return
    self.use_wikipedia = use_wikipedia

    self.new_keys = new_keys
    self.old_keys = old_keys
    self.text_ = text
    
    self.min_wpm = 25
    self.min_accuracy = 50
    self.min_chars = 200
    self.max_chars = 400

  def FindRandomArticle(self):
    self.text_ = self._FindRandomArticleText()

  def SetOptions(self, parent):
    attrs = ['allow_errs', 'ignore_accent', 'ignore_case', 'ignore_whitespace', 'space_is_return']
    for attr in attrs:
      setattr(parent, attr, getattr(self, attr))
      button_name = attr + '_check'
      if hasattr(parent, button_name):
        button = getattr(parent, button_name)
        button.set_active(getattr(self, attr))
      else:
        logging.info('Skipping %s' % button_name)
     
  def _FindRandomArticleText(self):
    fname = GetRandomArticle(self.pathname, self.lang)
    fi = gzip.open(fname, 'r')
    article = yaml.load(fi)
    self.cur_article = article
    fi.close()
    for title, sections in article.sections:
      for para in sections:
        if self.IsAcceptablePara(para):
          return article.page, title, para
        else:
          self.NotAcceptableParas(para)
    # Try again
    logging.info('Not found in %s, try again' % fname)
    return self._FindRandomArticleText()

  def _TwoKeyMedley(self, style=0):
    """Creates a simple combination for learning two characters.
    Returns:
      Ex. fff fff fff jjj jjj jjj fff jjj fff jjj ff jj ff jj ff jj fj fj jf jf fjf fjf jfj jfj
    """
    medley = [
      '000', '000', '000',
      '111', '111', '111',
      '000', '000',
      '111', '111',
      '00', '00',
      '11', '11',
      '00', '11', '00', '11',
      '01', '01', '10', '10',
      '010', '010', '010', 
      '101', '101', '101'
    ]
    assert len(self.new_keys) == 2
    return self._ApplyMedley(medley, self.FromToKbd(self.new_keys))

  def _OneHandMedley(self, style=0):
    """Creates a simple combination for learning for one hand (5 characters).
    Returns:
      Ex. aaa aaa sss sss ddd ddd fff fff ggg ggg
          asdfg asdfg asdfg
          gg ff dd ss aa
          aa ss dd ff gg
          gfdsa gfdsa gfdsa
    """
    medley = [
      '000', '000', '111', '111', '222', '222', '333', '333', '444', '444',
      '01234', '01234', '01234',
      '44', '33', '22', '11', '00',
      '00', '11', '22', '33', '44',
      '43210', '43210', '43210',
    ]
    assert len(self.old_keys) == 5
    return self._ApplyMedley(medley, self.FromToKbd(self.old_keys))
  
  def _TwoHandMedley(self, style=1):
    """Creates a simple combination for learning for two hands on one row (10 characters).
    Args:
      style: Numeric value indicating the sequence to use.
    Returns:
      Ex. aaa sss ddd fff ggg hhh jjj lll ;;;
          ;;; lll kkk hhh ggg fff ddd sss aaa 
          asdfg hjkl; asdfg hjkl;
          ;lkjh gfdsa ;lkjh gfdsa
          asdfg ;lkjh hjkl; gfdsa
    """
    medley = [[
        '000', '111', '222', '333', '444', '555', '666', '777', '888', '999',
        '999', '888', '777', '666', '555', '444', '333', '222', '111', '000',
        '01234', '56789', '01234', '56789',
        '98765', '43210', '98765', '43210',
        '01234', '98765', '01234', '98765',
      ], [
        '45', '36', '27', '18', '09',
        '45', '36', '27', '18', '09',
        '09', '18', '27', '36', '45',
        '09', '18', '27', '36', '45',
        '05', '16', '27', '38', '49',
        '94', '83', '72', '61', '50',
      ], [
        '02468', '02468', '13579', '13579',
        '86420', '86420', '97531', '97531',
        '45', '36', '27', '18', '09',
        '54', '63', '72', '81', '90',
      ],
    ]
    assert len(self.old_keys) == 10
    return self._ApplyMedley(medley[style - 1], self.FromToKbd(self.old_keys))

  def _ApplyMedley(self, medley, keys):
    ret = []
    for med in medley:
      x = []
      for ch in med:
        i = int(ch)
        x.append(keys[i])
      ret.append(''.join(x))
    return ' '.join(ret)

  def _BiGramRandom(self):
    if self.debug:
      num_chars = 10  # Type less when testing
    else:
      num_chars = self.min_chars
    keys = self.FromToKbd(self.new_keys + self.old_keys)
    if ' ' not in keys:
      keys += ' '
    ret = self._RandWords(keys, num_chars)
    return ret

  def _ForChars(self, chars):
    if self.lang in STATS:
      s = STATS[self.lang]
    else:
      s = Stats(self.lang)
    return s.GetForChars(chars)

  def _RandWords(self, chars, size):
    """Return random words base on bigram frequency.
    Uses only the chars listed above.
    """
    s = self._ForChars(chars)
    c = s.RandChar()
    l = [c]
    while len(l) < size:
      c = s.RandBiChar(c)
      if c == ' ' and l[-1] == ' ':
        # Don't have two spaces in a row
        continue
      l.append(c)
    if l[-1] == ' ':
      # Don't end on a space.
      l[-1] = s.RandChar();
    return ''.join(l)

  def _RandWord(self):
    word_len = self._RandWordLen()
    ret = []
    for i in range(word_len):
      if self._RandUseNewKey():
        if self.new_keys:
          ret.append(random.choice(self.FromToKbd(self.new_keys)))
        else:
          ret.append(random.choice(self.FromToKbd(self.old_keys)))
      else:
        if self.old_keys:
          ret.append(random.choice(self.FromToKbd(self.old_keys)))
        else:
          ret.append(random.choice(self.FromToKbd(self.new_keys)))
    return ''.join(ret)
    
  def _RandUseNewKey(self):
    return random.random() > 0.8

  def _RandWordLen(self):
    wl = int(random.gauss(4, 0.8))
    if wl < 1:
      wl = 1
    if wl > 10:
      wl = 10
    return wl

  def IsAcceptablePara(self, para):
    length = len(para)
    if length > self.max_chars or length < self.min_chars:
      return False
    ok_chars = dict((x, True) for x in self.old_keys)
    for ch in para:
      if ch not in ok_chars:
        return False
    return True

  def NotAcceptableParas(self, para):
    length = len(para)
    if length > self.max_chars:
      logging.info('Para too large %d > %d' % (length, self.max_chars))
      return
    elif length < self.min_chars:
      logging.info('Para too small %d < %d' % (length, self.min_chars))
      return
    ok_chars = dict((x, True) for x in self.old_keys)
    for ch in para:
      if ch not in ok_chars:
        logging.info( 'Char %r is not acceptable' % ch)
        return
    return

  @property
  def title(self):
    if not self.cur_article:
      return ''
    return _(self.cur_article.title)

  @property
  def preamble_text(self):
    if not self.preamble:
      return ''
    return self._AddStrings(self.preamble)

  @property
  def postamble_text(self):
    if not self.postamble:
      return ''
    return self._AddStrings(self.postamble)

  @property
  def instructions_text(self):
    if not self.instructions:
      return ''
    return self._AddStrings(self.instructions)

  def _AddStrings(self, str):
    self._AddNewKeys()
    str = _(str)
    while '%(' in str:
      str = str % self.strings
    return str

  def FromToKbd(self, lst):
    return [self.CharFromToKbd(c) for c in lst]

  def CharFromToKbd(self, ch):
    return self.to_kbd.ScanCodesToChar(self.us_kbd.CharToScanCodes(ch))

  def _AddNewKeys(self):
    for index in range(len(self.new_keys)):
      self.strings['key_%d' % index] = self.CharFromToKbd(self.new_keys[index])

  def MaybeNumeric(self, string):
    """Clean up the string, if it's a number conver to a number."""
    string = string.strip()
    if not string.isdigit():
      return string
    if '.' in string:
      return float(string)
    return int(string)

  def MakeArgs(self, args_str):
    lst = [self.MaybeNumeric(x) for x in args_str.split(',')]
    if len(lst) == 1 and lst[0] == '':
      lst = []
    return lst

  def _GetLessonText(self):
    re_text_function = re.compile(r'([a-zA-Z_]\w*)\((.*)\)')
    if not self.text_ or self.use_wikipedia:
      if self.use_wikipedia:
        title, section, self.text_ = self._FindRandomArticleText()
        self.instructions = unicode()
        self.instructions += _('You are typing the Wikipedia article: ') + title
        self.instructions += _(', subsection: ') + unicode(section)
        self.postamble_text = _(u'You just typed a paragraph from the Wikipedia article: ')
        self.postamble_text += title + _(u', subsection: ') + section
      elif self.text and re_text_function.search(self.text):
        func, args = re_text_function.search(self.text).groups()
        args = self.MakeArgs(args)
        func = '_' + func
        try:
          self.text_ = getattr(self, func)(*args)
        except Exception, e:
          print '\nException in: %s(%s)' % (func, ', '.join(str(x) for x in args))
          raise e
      elif len(self.new_keys) == 2 and len(self.old_keys) == 0:
        self.text_ = self._TwoKeyMedley()
      else:
        self.text_ = self._BiGramRandom()
    return self.text_
  lesson_text = property(_GetLessonText)

  def PrettyPrintOut(self, fo, method, previous):
    text = getattr(self, method)
    if method not in previous or previous[method] != text:
      fo.write('\n%s: %s' % (method, text))
    previous[method] = text

  def PrettyPrint(self, fo, index, previous):
    fo.write('------------------------------------------\n')
    fo.write('Lesson: %d' % index)
    self.PrettyPrintOut(fo, 'preamble_text', previous)
    self.PrettyPrintOut(fo, 'instructions_text', previous)
    self.PrettyPrintOut(fo, 'lesson_text', previous)
    self.PrettyPrintOut(fo, 'postamble_text', previous)
    self.PrettyPrintOut(fo, 'allow_errs', previous)
    self.PrettyPrintOut(fo, 'ignore_accent', previous)
    self.PrettyPrintOut(fo, 'ignore_case', previous)
    self.PrettyPrintOut(fo, 'ignore_whitespace', previous)
    self.PrettyPrintOut(fo, 'space_is_return', previous)
    self.PrettyPrintOut(fo, 'use_wikipedia', previous)
    fo.write('\n')


class StatsForChars:
  def __init__(self, lang, chars, raw_freq, raw_bi):
    self.lang = lang
    if isinstance(chars, list):
      self.chars = ''.join(chars)
    else:
      self.chars = chars
    self.freq = self.FilterRawFreq(raw_freq)
    self.bi = self.FilterRawBi(raw_bi)

  def FilterRawFreq(self, raw):
    lst = []
    nsum = 0
    chars = self.chars.replace(' ', '')  # remove the space
    for chr, count in raw:
      if chr in chars:
        nsum += count
        lst.append((nsum, chr))
    return lst

  def FilterRawBi(self, raw):
    dct = {}
    for chrs, count in raw:
      c1, c2 = chrs[0], chrs[1]
      if c1 in self.chars and c2 in self.chars:
        if c1 in dct:
          nsum = dct[c1][-1][0] + count
        else:
          nsum = count
          dct[c1] = []
        dct[c1].append((nsum, c2))

    #self.PrettyDict(dct)
    return dct

  def PrettyDict(self, dct):
    for c in sorted(dct.keys()):
      print c
      prev = 0
      for count, ch in dct[c]:
        delta = count - prev
        prev = count
        print delta, ch
    #import pprint
    #pprint.pprint(dct)

  def RandChar(self):
    n = random.randint(0, self.freq[-1][0])
    for nsum, char in self.freq:
      if nsum >= n:
        return char

  def RandBiChar(self, prev):
    clist = self.bi[prev]
    n = random.randint(0, clist[-1][0])
    for nsum, char in clist:
      if nsum >= n:
        return char
      
class Stats:
  def __init__(self, lang):
    self.lang = lang
    self.raw_freq = []
    self.raw_bi = []
    self.chars = None
    self.freq = []
    self.bi = []
    self.pathname = os.path.dirname(__file__)
    fname = 'stats/%s-freq-stats.txt' % self.lang
    self.LoadFreq(os.path.join(self.pathname, fname))
    fname = 'stats/%s-bigram-stats.txt' % self.lang
    self.LoadBiGram(os.path.join(self.pathname, fname))

  def LoadFreq(self, fname):
    self.raw_freq = []
    for line in codecs.open(fname, 'r', 'utf-8'):
      line = line.rstrip()
      ch = line[0]
      count = int(line[2:])
      if ch:
        self.raw_freq.append((ch, count))

  def LoadBiGram(self, fname):
    self.raw_bi = []
    for line in codecs.open(fname, 'r', 'utf-8'):
      bi = line[0:2]
      count = int(line[3:])
      if bi:
        self.raw_bi.append((bi, count))

  def GetForChars(self, chars):
    return StatsForChars(self.lang, chars, 
        self.raw_freq, self.raw_bi)

def GetRandomArticle(pathname, lang):
  dir = os.path.join(pathname, 'articles', lang)
  dirs = os.listdir(dir)
  rand_index = random.randint(0, len(dirs) - 1)
  dir = os.path.join(dir, dirs[rand_index])
  files = os.listdir(dir)
  rand_index = random.randint(0, len(files) - 1)
  fname = os.path.join(dir, files[rand_index])
  return fname

