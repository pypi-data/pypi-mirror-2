#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""gtk.Label with a image background."""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import gobject
import gtk

class PrettyLabel(gtk.Label):
  """Label with a background image (possibly svg)."""
  def __init__(self, fname):
    gtk.Label.__init__(self)
    self.pixbuf = None
    self.fname = fname

  @classmethod
  def Register(self):
    """Register the class as a Gtk widget."""
    gobject.type_register(PrettyLabel)
   
  def _LoadImage(self):   
    # load the image
    self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.fname)
    self.image_width = self.pixbuf.get_width()
    self.image_height = self.pixbuf.get_height()

  def do_realize(self):
    gtk.Label.do_realize(self)

    self.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))

    if not self.pixbuf:
      self._LoadImage()

    self._CenterTextVertically()
    self.queue_resize()

  def do_expose_event(self, event):
    """This is where the widget must draw itself."""

    align = self.get_alignment()
    gc = self.style.fg_gc[gtk.STATE_NORMAL]
    rect = event.area
    xy = self.get_allocation()
    deltay = rect.y - xy.y
    deltax = rect.x - xy.x
    rect.x += (xy.width * align[0] - self.image_width / 2.0) - deltax
    rect.y += (xy.height * align[0] - self.image_height / 2.0) - deltay
    self.window.draw_pixbuf(gc, self.pixbuf, 
        0, 0,
        rect.x, rect.y,
        self.image_width, self.image_height)
    gtk.Label.do_expose_event(self, event)

  def do_size_request(self, requisition):
    """From Widget.py: The do_size_request method Gtk+ is calling
     on a widget to ask it the widget how large it wishes to be. 
     It's not guaranteed that gtk+ will actually give this size 
     to the widget.  So we will send gtk+ the size needed for
     the maximum amount of stars"""
    if not self.pixbuf:
      self._LoadImage()
    # First get the size that the text wants to get the text size
    gtk.Label.do_size_request(self, requisition)
    self.text_width = requisition.width
    self.text_height = requisition.height

    # Set the our image size
    requisition.height = self.image_height
    requisition.width = self.image_width

    # Set the our image size
    requisition.height = self.image_height
    requisition.width = self.image_width

  def _CenterTextVertically(self):
    ydelta = int(self.image_height / 2.0 - self.text_height / 2.0)
    self.set_padding(-1, ydelta)


def Main():
  PrettyLabel.Register()
  win = gtk.Window()
  win.resize(89, 106)
  win.connect('delete-event', gtk.main_quit)

  prettyLabel = PrettyLabel('status.svg')
  prettyLabel.set_use_markup(True)
  prettyLabel.set_width_chars(19)
  prettyLabel.set_text('0.0 wpm')
  win.add(prettyLabel)

  win.show_all()
  gtk.main()


if __name__ == '__main__':
  Main()
