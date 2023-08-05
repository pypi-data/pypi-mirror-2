#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""gtk.HButtonBox with a image background.

TODO(scottkirkwood): This probably should be used as a base for my_dialog and pretty_label.
"""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import gobject
import gtk
import lazy_pixbuf_creator
import logging


class ImageBackedWidget(gtk.HButtonBox):
  """Label with a background image (possibly svg)."""
  def __init__(self, fname):
    gtk.HButtonBox.__init__(self)
    # This setting redraws the window properly on some resizing.
    self.set_redraw_on_allocate(True)
    self.set_homogeneous(False)
    self.pixbuf = None
    self.fname = fname
    self.lazy = lazy_pixbuf_creator.LazyPixbufCreator({'widget': [
          self.fname]}, resize=1.0)

  @classmethod
  def Register(self):
    """Register the class as a Gtk widget."""
    gobject.type_register(ImageBackedWidget)

  def _LoadImage(self):
    # load the image
    self.pixbuf = self.lazy.Get('widget')
    self.image_width = self.pixbuf.get_width()
    self.image_height = self.pixbuf.get_height()
    logging.info('Image size %dx%d' % (self.image_width, self.image_height))

  def do_realize(self):
    gtk.HButtonBox.do_realize(self)
    if not self.pixbuf:
      self._LoadImage()

    self.queue_resize()

  def do_expose_event(self, event):
    """This is where the widget must draw itself."""
    gc = self.style.fg_gc[gtk.STATE_NORMAL]
    rect = event.area
    xy = self.get_allocation()
    deltay = rect.y - xy.y
    deltax = rect.x - xy.x
    self.window.draw_pixbuf(gc, self.pixbuf,
        deltax, deltay,
        rect.x, rect.y,
        min(self.image_width, rect.width), min(self.image_height, rect.height))
    gtk.HButtonBox.do_expose_event(self, event)

  def do_size_request(self, requisition):
    """From Widget.py: The do_size_request method Gtk+ is calling
     on a widget to ask it the widget how large it wishes to be.
     It's not guaranteed that gtk+ will actually give this size
     to the widget.  So we will send gtk+ the size needed for
     the maximum amount of stars"""
    if not self.pixbuf:
      self._LoadImage()

    # First get the size that the text wants to get the text size
    gtk.HButtonBox.do_size_request(self, requisition)
    self.text_width = requisition.width
    self.text_height = requisition.height

    # Set the our image size
    requisition.height = self.image_height
    requisition.width = self.image_width

    # Set the our image size
    requisition.height = self.image_height
    requisition.width = self.image_width
    

def Main():
  ImageBackedWidget.Register()
  win = gtk.Window()
  win.resize(800, 100)
  win.connect('delete-event', gtk.main_quit)

  imageBackedWidget = ImageBackedWidget('options.svg')
  imageBackedWidget.set_flags(imageBackedWidget.flags() & ~gtk.CAN_FOCUS)
  vbox = gtk.VBox(homogeneous=False, spacing=0)
  checkbox = gtk.CheckButton('Ignore Case')
  checkbox.show()
  vbox.pack_start(checkbox, expand=True, fill=True)
  checkbox = gtk.CheckButton('Ignore accent')
  checkbox.show()
  vbox.pack_start(checkbox, expand=True, fill=True)
  checkbox = gtk.CheckButton('Ignore Whitespace')
  checkbox.show()
  vbox.pack_start(checkbox, expand=True, fill=True)
  vbox.show()
  imageBackedWidget.pack_start(vbox, expand=False, fill=False)
  
  vbox = gtk.VBox(homogeneous=False, spacing=0)
  checkbox = gtk.CheckButton('Allow errors')
  checkbox.show()
  vbox.pack_start(checkbox, expand=True, fill=True)
  vbox.show()
  imageBackedWidget.pack_start(vbox, expand=False, fill=False)

  imageBackedWidget.show_all()

  hbox = gtk.HBox()
  hbox.pack_start(imageBackedWidget, expand=True, fill=False)
  hbox.show()

  win.add(hbox)
  win.show_all()
  gtk.main()

if __name__ == '__main__':
  Main()
