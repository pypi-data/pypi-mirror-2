#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""Code to load in a lesson plan for use.

I'm using the scan codes because it's more important the positions than the keys.
"""

import lesson

import codecs
import copy
import gettext
import glob
import gzip
import logging
import scancodes
import os
import sys
import yaml

ACCEPTABLE_CHARS = {
  'en': list(u'abcdefghijklmnopqrstuvwxyz'
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
              '0123456789'
              ' ,.-"\')('    # Most frequent
              ':;/%[]$&!=?'  # Less frequent
              '*@`~^_+{}\\|<>' # Even less frequent but easily accessible
            ), 
           # By frequency only
  'pt_BR': list(u' aeosridntmuclp,vgf.bhãqçéAáíz1C-E0xjPóSM90O"2T)ê(NIõBDRGFúkL583V4à6J7y:UHâôw;WXK'),
}

class Lessons:
  """Class which holds a list of lessons for a language."""
  def __init__(self, lang, kbd, debug):
    self.lang = lang
    self.debug = debug
    self.lessons = []
    self.lesson_index = 0
    self.level_index = 0
    self.pathname = os.path.dirname(__file__)
    self.us_kbd = scancodes.ScanCodes()
    self.us_kbd.ReadFile(os.path.join(self.pathname, 'us.kbd'))
    self.to_kbd = kbd

  def ReadLessons(self, dir):
    fname = 'beginner-lessons.yaml'
    self.lessons.append(self._ReadLessonFile(os.path.join(dir, fname)))
    self.lessons.append([
      lesson.Lesson(us_kbd=self.us_kbd, to_kbd=self.to_kbd,
                    lang=self.lang,
                    use_wikipedia=True,
                    debug=self.debug,
                    old_keys=ACCEPTABLE_CHARS[self.lang])])

  def _ReadLessonFile(self, fname):
    yml = yaml.load(open(fname, 'r'))
    lessons = []
    self.strings = yml['strings']
    for item in yml['lessons']:
      if lessons:
        alesson = copy.deepcopy(lessons[-1])
      else:
        alesson = lesson.Lesson(us_kbd=self.us_kbd, to_kbd=self.to_kbd, 
                                lang=self.lang, strings=self.strings, debug=self.debug)
      for key, val in item.items():
        setattr(alesson, key, val)
      lessons.append(alesson)
    return lessons

  def NumLessons(self):
    return len(self.lessons)

  def NumLevels(self):
    """Num Levels for this lesson."""
    return self.NumLevelsAt_(self.lesson_index)

  def NumLevelsAt_(self, alesson):
    return len(self.lessons[alesson])

  def CurLesson(self):
    return self.lessons[self.lesson_index][self.level_index]

  def NextLesson(self):
    self.level_index += 1
    if self.level_index >= self.NumLevels():
      if self.lesson_index < self.NumLessons() - 1:
        self.lesson_index += 1
        self.level_index = 0
      else:
        self.level_index = self.NumLevels() - 1
    return self.CurLesson()

  def SetLesson(self, alesson, level):    
    assert alesson < self.NumLessons()
    self.lesson_index = alesson
    assert level < self.NumLevels()
    self.level_index = level
    logging.info('Set lesson to %d:%d' % (self.lesson_index, self.level_index))
    return self.CurLesson()

  def PotOut(self, fo, str, comment):
    if not str:
      return
    fo.write('# %s\n' % comment)
    fo.write('msgid "%s"\n' % str.replace('\n', r'\n'))
    fo.write('msgstr ""\n\n')

  def PotStrings(self, fo, lesson, index):
    ret = {}
    context = 'lesson %03d' % index
    if lesson.instructions:
      ret.update({lesson.instructions: '%s - instruction' % context})
    if lesson.preamble:
      ret.update({lesson.preamble: '%s - preamble' % context})
    if lesson.postamble:
      ret.update({lesson.postamble: '%s - postamble' % context})
    return ret

  def AppendPotFile(self, pot_fname):
    fo = codecs.open(pot_fname, 'a', 'utf-8')
    print 'Appending POT to %s' % pot_fname
    strs = {}
    cur_lesson = self.CurLesson()
    strings = cur_lesson.strings
    for index, key in enumerate(strings):
      strs.update({strings[key]: '_string %03d' % index})
    index = 1
    strs.update(self.PotStrings(fo, cur_lesson, index))
    while self.NextLesson() != cur_lesson:
      cur_lesson = self.CurLesson()
      index += 1
      strs.update(self.PotStrings(fo, cur_lesson, index))
    tosort = list((y, x) for x, y in strs.items())
    tosort.sort()
    for comment, str in tosort:
      self.PotOut(fo, str, comment)

  def WriteSampleFile(self, out_fname):
    fo = codecs.open(out_fname, 'w', 'utf-8')
    print 'Outputing to %s' % out_fname
    self.WriteSampleOut(fo)

  def WriteSampleOut(self, fo):
    cur_lesson = self.CurLesson()
    index = 1
    previous = {}
    cur_lesson.PrettyPrint(fo, index, previous)
    while self.NextLesson() != cur_lesson:
      index += 1
      cur_lesson = self.CurLesson()
      cur_lesson.PrettyPrint(fo, index, previous)

if __name__ == '__main__':
  import optparse

  parser = optparse.OptionParser()
  parser.add_option('-l', '--lang', dest='lang', default='en',
      help='Language file to use ex: "en"')
  parser.add_option('-k', '--kbd', dest='kbd', default='us',
      help='Keyboard file to use ex: "us"')
  parser.add_option('-o', '--out', dest='out_fname',
      help='Output filename "sample.txt"')
  parser.add_option('--pot', dest='pot_fname',
      help='Output gettext POT filename "locale/key-train.pot"')
  options, args = parser.parse_args()
  kbd = scancodes.ScanCodes()
  kbd.ReadFile('%s.kbd' % options.kbd)
  pathname = os.path.dirname(__file__)
  if options.lang != 'en':
    gettext_lang = gettext.translation('key-train', os.path.join(pathname, 'locale'),
                                       languages=[options.lang])
    gettext_lang.install(unicode=True)
  else:
    gettext.install('key-train', 'locale') 
  lessons = Lessons(options.lang, kbd, False)
  lessons.ReadLessons('.')
  if options.out_fname:
    lessons.WriteSampleFile(options.out_fname)
  if options.pot_fname:
    lessons.AppendPotFile(options.pot_fname)
