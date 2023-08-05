#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""gtk.Dialog with extra handling and an SVG image background.

The action buttons are disabled for a period of time because there is a chance that the typist
is furiously typing and hits the spacebar, thus dismissing the dialog.
"""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import gobject
import gtk
import lazy_pixbuf_creator
import logging
from lxml import etree

class MyDialog(gtk.Dialog):
  """Dialog with an SVG background image."""
  def __init__(self, fname, title=None, parent=None, flags=0, buttons=None,
      from_to={}):
    gtk.Dialog.__init__(self, title, parent, flags, buttons)
    self.pixbuf = None
    self.fname = fname
    self.fixed = gtk.Fixed()
    self.ids = {}
    self.from_to = from_to
    self.lazy = lazy_pixbuf_creator.LazyPixbufCreator({'dialog': [
          FixSvgKeyClosure(self.ids, fname)
          ]}, resize=1.0)
    self.vbox.add(self.fixed)
    self.fixed.show()
    gobject.timeout_add(600, self.EnableButtons)

  def CreateLabels(self):
    for label, p in self.ids.items():
      x, y, w, h = p['pos']
      l = gtk.Label()
      l.set_line_wrap(True)
      l.set_selectable(False)
      l.set_single_line_mode(False)
      l.set_size_request(w, h)
      #l.set_markup('<span size="15000"><b>Bob was lorem ipsum</b> lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum.</span>')
      txt = self.from_to[label]
      l.set_markup('<span size="13000">%s</span>' % txt)
      l.show()
      self.fixed.put(l, x, y)
      p['label'] = l

  @classmethod
  def Register(self):
    """Register the class as a Gtk widget."""
    gobject.type_register(MyDialog)

  def EnableButtons(self):
    if not self.action_area:
      return
    for child in self.action_area.get_children():
      child.set_sensitive(True)
      child.grab_focus()

  def _LoadImage(self):
    # load the image
    self.pixbuf = self.lazy.Get('dialog')
    self.image_width = self.pixbuf.get_width()
    self.image_height = self.pixbuf.get_height()
    self.CreateLabels()

  def do_realize(self):
    # diable the button(s)
    for child in self.action_area.get_children():
      child.set_sensitive(False)

    gtk.Dialog.do_realize(self)

    if not self.pixbuf:
      self._LoadImage()

    self.queue_resize()

  def do_expose_event(self, event):
    """This is where the widget must draw itself."""
    retval = gtk.Dialog.do_expose_event(self, event)
    gc = self.style.fg_gc[gtk.STATE_NORMAL]
    rect = event.area
    xy = self.get_allocation()
    deltay = rect.y - xy.y
    deltax = rect.x - xy.x
    rect.x += - deltax
    rect.y += - deltay
    self.window.draw_pixbuf(gc, self.pixbuf,
        0, 0, rect.x, rect.y, self.image_width, self.image_height)
    self.vbox.do_expose_event(self.vbox, event)

  def do_size_request(self, requisition):
    """From Widget.py: The do_size_request method Gtk+ is calling
     on a widget to ask it the widget how large it wishes to be.
     It's not guaranteed that gtk+ will actually give this size
     to the widget.  So we will send gtk+ the size needed for
     the maximum amount of stars"""
    if not self.pixbuf:
      self._LoadImage()

    # First get the size that the text wants to get the text size
    gtk.Dialog.do_size_request(self, requisition)
    self.text_width = requisition.width
    self.text_height = requisition.height
    
    button_height = 50
    # Set the our image size
    requisition.height = self.image_height + button_height
    requisition.width = self.image_width


def FixSvgKeyClosure(ids, fname):
  """Create a closure to modify the key.
  Args:
    ids: dictionary of ids to (x, y, w, h)
  Returns:
    A bound function which returns the file fname with modifications.
  """

  def FixSvgKey():
    """Given an SVG file return the SVG text fixed."""
    logging.debug('Read file %r' % fname)
    f = open(fname)
    bytes = f.read()
    f.close()
    tree = etree.fromstring(bytes)
    for element in tree.getiterator('{http://www.w3.org/2000/svg}rect'):
      id = element.get('id')
      if id and id.startswith('LABEL_'):
        x = int(float(element.attrib['x']))
        y = int(float(element.attrib['y']))
        w = int(float(element.attrib['width']))
        h = int(float(element.attrib['height']))
        label = id.replace('LABEL_', '')
        ids[label] = { 'pos': (x, y, w, h), 'label': None }
    return bytes

  return FixSvgKey

def Main():
  MyDialog.Register()

  myDialog = MyDialog(
      'finished.svg', 'Finished', None,
       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
       (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE),
       {'text':'text',
        'raw_wpm': '%.0f words per minute' % 60.0,
        'accuracy_percent': '%.0f%% accurate' % 98.0,
        'net_wpm': '%.0f net words per minute' % 55.0})
  myDialog.resize(300, 200)
  
  myDialog.show_all()
  myDialog.run()

if __name__ == '__main__':
  Main()
