#!/usr/bin/python
# 

"""Handling keyboard drawing."""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import pygtk
pygtk.require('2.0')
import gtk
import scancodes
import time
import logging
import key_positions

class KeyboardImage(gtk.Image):
  def __init__(self, pixbufs, name):
    gtk.Image.__init__(self)
    self.dirty_rects = []
    self.pixbufs = pixbufs
    self._SwitchTo(name)

  def SwitchTo(self, name):
    if name != self.current:
      self._SwitchTo(name)
      return True
    return False

  def InvalidateRect(self, x, y, w, h):
    self.queue_draw_area(x, y, w, h)
    #self.queue_draw_area(x, y, w, h)
    
  def _SwitchTo(self, name):
    self.set_from_pixbuf(self.pixbufs.Get(name))
    self.current = name
    self.show()

  def DrawScanCode(self, scancode, style):
    if self.SwitchImage(scancode):
      self.queue_draw()
      self.DrawDirtyRects()
    x, y, w, h = self.GetXYWHForScancode(scancode)
    logging.info('Draw rect %d, %d, %d, %d for scancode %d' % (x, y, w, h, scancode))
    if not w or not h:
      logging.info('Unknown scancode %d' % scancode)
      return
    rect = (x, y, w, h)
    if rect not in self.dirty_rects:
      self.DrawDirtyRects()

    self._DrawRect(rect, style)

  def DrawScanCodes(self, scancodes, style):
    #self.DrawDirtyRects()
    for scancode in scancodes:
      x, y, w, h = self.GetXYWHForScancode(scancode)
      logging.info('Draw rect %d, %d, %d, %d for scancodes %d' % (x, y, w, h, scancode))
      if not w or not h:
        logging.info('Unknown scancode %d' % scancode)
        return
      rect = (x, y, w, h)
      self._DrawRect(rect, style)

  def _DrawRect(self, rect, style):
    x, y, w, h = rect
    cr = self.parent.window.cairo_create()
    if style:
      cr.set_source_rgba(1, 0, 0, .5)
      cr.set_line_width(7)
      inset = 0
    else:
      cr.set_line_width(7)
      cr.set_source_rgba(0, 1, 0, .9)
      inset = 4
    self.RoundedRect(cr, x + inset, y + inset, w - inset * 2, h - inset * 2, 11)
    cr.stroke()
    self.dirty_rects.append(rect)
 
  def SwitchImage(self, scancode):
    if scancode in [30, 31, 32, 33, 36, 37, 38, 39]:
      return self.SwitchTo('home')
    elif scancode in [18, 23, 34, 35]:
      return self.SwitchTo(str(scancode))    
    else:
      return self.SwitchTo('home')

  def KeyUp(self, hardware_keycode):
    scancode = scancodes.ToMyScanCode(hardware_keycode)
    x, y, w, h = self.GetXYWHForScancode(scancode)
    if w:
      self.InvalidateRect(x - 2, y - 2, w + 3, h + 3)

  def RoundedRect(self, cr, x0, y0, w, h, radius):
    x1 = x0 + w;
    y1 = y0 + h;
    if not w or not h:
      return
    cr.move_to(x0, y0 + radius)
    cr.curve_to(x0, y0, x0, y0, x0 + radius, y0)
    cr.line_to(x1 - radius, y0)
    cr.curve_to(x1, y0, x1, y0, x1, y0 + radius)
    cr.line_to(x1 , y1 - radius)
    cr.curve_to(x1, y1, x1, y1, x1 - radius, y1)
    cr.line_to(x0 + radius, y1)
    cr.curve_to(x0, y1, x0, y1, x0, y1- radius)
    cr.line_to(x0, y0 + radius)
    cr.close_path

  def GetXYWHForScancode(self, keycode):
    if keycode in key_positions.KEY_POSITIONS:
      x, y, w, h = key_positions.KEY_POSITIONS[keycode]
    else:
      return 0, 0, 0, 0
    dx, dy, = 1, -5 
    smaller_w, smaller_h = 1, 2
    alloc = self.allocation
    return x + dx + alloc.x, y + dy + alloc.y, w - smaller_w, h - smaller_h

  def DrawDirtyRects(self):
    for x, y, w, h in self.dirty_rects:
      self.InvalidateRect(x - 2, y - 2, w + 3, h + 3)
    self.dirty_rects = []

  def CapslockWarning(self):
    logging.warning('CapsLock on')
    self.DrawScanCode(58, True)


def Main():
  import lazy_pixbuf_creator 
  import optparse
  parser = optparse.OptionParser()
  (options, args) = parser.parse_args()

  win = gtk.Window()
  win.resize(89, 106)
  win.connect('delete-event', gtk.main_quit)
  name_fnames = {
    'kbd': ['keyboard.svg'],
    'home': ['keyboard.svg', 'images/home.svg'],
    '34': ['keyboard.svg', 'images/34.svg'],  # g
  }
  pixbufs = lazy_pixbuf_creator.LazyPixbufCreator(name_fnames, 1.0)
  keyboard_image = KeyboardImage(pixbufs, 'home')
  keyboard_image.show_all()
  win.add(keyboard_image)

  win.show_all()
  gtk.main()


if __name__ == "__main__":
  Main()
