#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

import codecs
import gettext
import os
import random
import sys
import unittest
import StringIO

import lesson
import lessons
import scancodes


class TestLessons(unittest.TestCase):
  def setUp(self):
    self.pathname = os.path.dirname(__file__)

  def OutLesson(self, lang, kbd_fname, fo):
    kbd = scancodes.ScanCodes()
    kbd.ReadFile('%s.kbd' % kbd_fname)
    if lang != 'en':
      gettext_lang = gettext.translation('key-train', os.path.join(self.pathname, 'locale'),
                                         languages=[lang])
      gettext_lang.install(unicode=True)
    else:
      gettext.install('key-train', 'locale') 
    random.seed(123)
    l = lessons.Lessons(lang, kbd, False)
    l.ReadLessons('.')
    l.WriteSampleOut(fo)
    
  def VerifyLesson(self, lang, kbd):
    current_fname = '%s-%s-current.txt' % (lang, kbd)
    fo = StringIO.StringIO()
    self.OutLesson(lang, kbd, fo)
    text_new = fo.getvalue()
    golden_fname = 'testdata/%s-%s-golden.txt' % (lang, kbd)
    fi = codecs.open(os.path.join(self.pathname, golden_fname), 'r', 'utf-8')
    text_golden = fi.read()
    fi.close()
    if text_golden != text_new:
      current_fname = '%s-%s-current.txt' % (lang, kbd)
      fo2 = codecs.open(current_fname, 'w', 'utf-8')
      fo2.write(text_new)
      fo2.close()
      print '%s does not match %s' % (current_fname, golden_fname)
      print 'tkdiff %s %s' % (current_fname, golden_fname)
      sys.exit(-1)

  def testEng(self):
    self.VerifyLesson('en', 'us')

  def testPtBr(self):
    self.VerifyLesson('pt_BR', 'pt_BR')

if __name__ == '__main__':
  unittest.main()
