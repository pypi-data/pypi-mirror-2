#!/usr/bin/python
#
# Copyright 2010 Scott Kirkwood All Rights Reserved.

"""Quickly create a kbd file by mashing keys.

Run it.
"""

__author__ = 'scott@forusers.com (Scott Kirkwood)'


import scancodes
import gtk

class CreateKbdFile:
  def __init__(self, old_file):
    win = gtk.Window()
    win.resize(800, 100)
    self.scancode = scancodes.ScanCodes()
    self.scancode.ReadFile('us.kbd')
    self.new_codes = {}
    if old_file:
      self.ReadOldFile(old_file)
    button = gtk.Button('Done')
    button.connect('released', self.Done)
    win.add(button)
    button.show()
    win.connect('delete-event', self.Quit)
    win.connect('key_press_event', self.KeyDown)
    win.show_all()

  def Done(self, widget):
    self.Quit(widget, None)
    
  def ReadOldFile(self, old_file):
    fi = open(old_file)
    for n, line in enumerate(fi):
      cols = line.rstrip().split(' ')
      if cols and cols[0].lstrip() == '#':
        continue
      scancode = int(cols[0])
      try:
        self.new_codes[scancode] = self.scancode.GrabData(cols)
      except Exception, e:
        print 'Error on line %d: %r' % (n + 1, e)
    fi.close()

  def KeyDown(self, widget, data):
    gtk_scancode = data.hardware_keycode
    my_scancode = scancodes.ToMyScanCode(gtk_scancode)
    ch = data.string
    shift_down = data.state & gtk.gdk.SHIFT_MASK
    if not my_scancode in self.new_codes:
      code_info = self.scancode.scancodes[my_scancode]
      self.new_codes[my_scancode] = { 
        'named': code_info['named'],
        'finger': code_info['finger'],
        'row': code_info['row'],
        'lower': '?',
        'upper': '?',
      }
      if len(code_info['lower']) > 1:
        self.new_codes[my_scancode]['lower'] = code_info['lower']
        self.new_codes[my_scancode]['upper'] = code_info['upper']
    if ch not in [' ', '\n', '\r', '\t', '\b', '\v', '\b', '\a', '\x1b']:
      if shift_down:
        self.new_codes[my_scancode]['upper'] = ch
      else:
        self.new_codes[my_scancode]['lower'] = ch
    print my_scancode, ch

  def PrintAll(self):
    fname = 'out.kbd'
    fo = file(fname, 'w')
    preamble = """# This is a space separated file with UTF-8 encoding
# Upper-Case name is optional.
# If toupper(lower) == upper then we display the upper name on the key ex. A
# Otherwise we display both (ex. & 7)
# Fingers are
# 1 - left pinky
# 2 - left ring finger
# 3 - left middle finger
# 4 - left index finger
# 5 - left thumb
# 6 - right thumb
# 7 - right index
# 8 - right middle
# 9 - right ring
# 10 - right pinkie
# Rows are:
# 3 - function key row
# 2 - number row
# 1 - qwerty row
# 0 - home row
# -1 - zxcv row
# -2 - space row.
# Scancode Map-Name Lower-Case Upper-Case Finger Row 
"""
    fo.write(preamble)
    for key, info in sorted(self.new_codes.items()):
      if 'finger' in info and info['finger']:
        fo.write('%d %s %s %s %s %s\n' % (key, info['named'], info['lower'], info['upper'],
                                          info['finger'], info['row']))
      else:
        fo.write('%d %s %s %s\n' % (key, info['named'], info['lower'], info['upper']))
    fo.close()
    print 'Written to %s' % fname

  def Quit(self, widget, evt):
    print 'Goodbye'
    self.PrintAll()
    gtk.main_quit()

def Main():
  import optparse
  parser = optparse.OptionParser()
  (options, args) = parser.parse_args()
  if len(args):
    old_file = args[0]
  else:
    old_file = None
  ckf = CreateKbdFile(old_file)
  gtk.main()

if __name__ == '__main__':
  Main()
