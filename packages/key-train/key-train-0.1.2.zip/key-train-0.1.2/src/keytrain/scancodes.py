#!/usr/bin/python
"""Read in a scan code table."""

import codecs
import os
import re
import sys

class ScanCodes:
  def __init__(self):
    self._Reset()

  def _Reset(self):
    self.char_to_scancodes = {}
    self.scancodes_to_char = {}
    self.scancodes = {}

  def ReadFile(self, fname):
    err_count = 0
    for n, line in enumerate(codecs.open(fname, 'r', 'utf-8')):
      cols = line.rstrip().split(' ')
      if cols and cols[0].lstrip() == '#':
        continue
      scancode = int(cols[0])
      try:
        self.scancodes[scancode] = self.GrabData(cols)
      except Exception, e:
        print 'Error on line %d: %r' % (n + 1, e)
        err_count += 1
    if err_count:
      sys.exit(-1)
    self.BuildCharToScancodes()

  def BuildCharToScancodes(self):
    for scancode, val in self.scancodes.items():
      lower = val['lower']
      upper = val['upper']
      finger = val['finger']
      if len(lower) > 1:
        continue
      if lower in self.char_to_scancodes:
        print 'The characer %r is defined twice %r' % (lower, val['named'])
        assert False
      self.char_to_scancodes[lower] = (scancode,)
      self.scancodes_to_char[(scancode,)] = lower
      if upper and upper != lower:
        if finger > 6:
          shift = 42  # left shift
        else:
          shift = 54  # right shift
        if upper in self.char_to_scancodes:
          print 'The upper characer %r is defined twice %r' % (upper, val['named'])
          assert False
        self.char_to_scancodes[upper] = (shift, scancode)
        self.scancodes_to_char[(shift, scancode)] = upper

  @classmethod 
  def GrabData(self, cols):
    scancode = int(cols[0])
    info = { 
      'named': '',
      'to_show': '',
      'lower': '',
      'upper': '',
      'finger': None,
      'row': None,
    }
    info['named'] = cols[1]
    info['lower'] = cols[2]
    if len(cols) == 3:
      info['to_show'] = cols[2]
      return info
    info['upper'] = cols[3]
    if info['lower'].upper() == info['upper']:
      info['to_show'] = info['upper']
    else:
      info['to_show'] = info['lower']
    if len(cols) <= 5:
      return info
    info['finger'] = int(cols[4])
    assert info['finger'] > 0 and info['finger'] < 11
    info['row'] = int(cols[5])
    assert info['row'] >= -2 and info['row'] <= 3
    if info['lower'] == 'Space':
      info['lower'] = ' '
      info['upper'] = ' '
    return info

  def CharToScanCodes(self, text):
    if text in self.char_to_scancodes:
      return self.char_to_scancodes[text]
    return []

  def ScanCodesToChar(self, codes):
    if codes in self.scancodes_to_char:
      return self.scancodes_to_char[codes]
    return ''
    
    
def PrettyPrint(scancodes):
  for key, val in scancodes.scancodes.items():
    print key, val['named'], val['to_show']


def ToMyScanCode(their_scan_code):
  if their_scan_code == 108:
    return 84
  # My scan codes are the same as their scan codes minus 8
  return their_scan_code - 8


if __name__ == '__main__':
  sc = ScanCodes()
  sc.ReadFile('us.kbd')
  PrettyPrint(sc)
