#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""gtk.TextView used to show instructions."""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import gobject
import pango
import gtk

class InstructionsBox(gtk.ScrolledWindow):
  """TextView used to show instructions."""
  def __init__(self):
    gtk.ScrolledWindow.__init__(self)

    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
    self.set_border_width(10)
    self.show()
    
    text_buffer = gtk.TextBuffer()
    self.textview = gtk.TextView()
    self.textview.show()
    self.textview.set_buffer(text_buffer)
    self.textview.set_left_margin(10)
    self.textview.set_right_margin(10)
    self.textview.set_pixels_above_lines(1)
    self.textview.set_pixels_below_lines(1)

    self.textview.set_editable(False)
    self.textview.set_cursor_visible(False)

    # We want to get the tab and not have it navigate to another control
    self.textview.set_accepts_tab(True)
    self.add(self.textview)

    # Set Font
    font = pango.FontDescription('Helvetica 11')
    self.textview.modify_font(font)
    self.textview.set_wrap_mode(gtk.WRAP_WORD)
    
  @classmethod
  def Register(self):
    """Register the class as a Gtk widget."""
    gobject.type_register(InstructionsBox)
  
  def SetText(self, txt):
    self.textview.get_buffer().set_text(txt)

  def SetBackground(self):
    color = 'white'
    self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
    self.textview.queue_draw()

def Main():
  InstructionsBox.Register()
  win = gtk.Window()
  win.resize(89, 106)
  win.connect('delete-event', gtk.main_quit)

  ib = InstructionsBox()
  ib.SetText('Here is some <b>sample text</b> which should wrap to the next line.\n'
             'Newlines separate paragraphs.')
  win.add(ib)

  win.show_all()
  gtk.main()


if __name__ == '__main__':
  Main()
