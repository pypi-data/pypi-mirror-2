#!/usr/bin/python

"""Handle dead key character combinations.

TODO: use https://help.ubuntu.com/community/GtkDeadKeyTable
which is more complete.
"""
import gtk
import logging

DEAD_KEYS = {
  gtk.keysyms.dead_tilde: '~',
  gtk.keysyms.dead_acute: '\'',
  gtk.keysyms.dead_circumflex: '^',
  gtk.keysyms.dead_grave: '`',
  gtk.keysyms.dead_doubleacute: '"',
}

COMBINER = {
  '~': {
    'a': u'\xe3',
    'A': u'\xc3',
    'o': u'\xf5',
    'O': u'\xd5',
  },
  '\'': {
    'c': u'\xe7',
    'C': u'\xc7',
    'a': u'\xe1', 
    'A': u'\xc1',
    'e': u'\xe9',
    'E': u'\xc9',
    'i': u'\xed',
    'I': u'\xcd',
    'o': u'\xf3',
    'O': u'\xd3',
    'u': u'\xfa',
    'U': u'\xda',
  },
  '^': {
    'a': u'\xe2',
    'A': u'\xc2',
    'e': u'\xea',
    'E': u'\xca',
    'o': u'\xf4',
    'O': u'\xd4',
  },
  '`': {
    'a': u'\xe0',
    'A': u'\xc0',
  },
  '"': {
    'a': u'\xe4',
    'A': u'\xc4',
    'e': u'\xeb',
    'E': u'\xcb',
    'u': u'\xfc',
    'U': u'\xdc',
    'o': u'\xf6',
    'O': u'\xd6',
  }
}

class DeadKey:
  def __init__(self):
    self.last_dead_key = None

  def WasDeadKey(self, keycode):
    if keycode in DEAD_KEYS:
      self.last_dead_key = DEAD_KEYS[data.keyval]
      logging.info('Dead key %d' % self.last_dead_key)
      return True
    return False

  def ConvertText(self, text):
    """Convert text ex. 'a' into something with an accent if previous was a deadkey."""
    if self.last_dead_key:
      if text in COMBINER[self.last_dead_key]:
        text = COMBINER[self.last_dead_key][txt]
        logging.info('Combining to %s' % txt)
      self.last_dead_key = None
    return text
