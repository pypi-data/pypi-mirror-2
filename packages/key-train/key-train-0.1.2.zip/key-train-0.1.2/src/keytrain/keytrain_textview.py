#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""gtk.TextView with a image background."""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import gobject
import pango
import gtk


class KeyTrainTextView(gtk.TextView):
  """TextView with a background color."""
  def __init__(self):
    gtk.TextView.__init__(self)
    self.lined_text = False

    self.connect('button-press-event', self.IgnoreButton)
    self.connect('key_press_event', self.IgnoreKeystrokes)
    if self.lined_text:
      self.connect("expose-event", self.expose_view)
    text_buffer = gtk.TextBuffer()
    self.set_buffer(text_buffer)

    # Margin
    self.set_left_margin(15)
    self.set_right_margin(15)
    self.set_pixels_above_lines(10)
    self.set_pixels_below_lines(10)

    self.set_editable(True)
    self.set_cursor_visible(True)
    # Also doesn't work
    #settings = self.window.get_settings()
    #settings.set_long_property('gtk-cursor-theme-size', 127, 'key-mon')

    # We want to get the tab and not have it navigate to another control
    self.set_accepts_tab(True)

    font = pango.FontDescription('Monospace 20')
    font.set_stretch(True)
    font.set_weight(pango.WEIGHT_BOLD)
    self.font_size = font.get_size() / pango.SCALE
    self.modify_font(font)
    self.set_wrap_mode(gtk.WRAP_WORD)
    self.SetStyles()
    self.SetBackground(False)
    self.drawable = None

  def expose_view(self, window, event):
    if not self.drawable:
      self.drawable = self.get_window(gtk.TEXT_WINDOW_TEXT)
    gc = self.drawable.new_gc()
    line_height = self.font_size + 13
    vadjust = 0
    vadjust = self.get_parent().get_vadjustment().get_value()
    y = 10 + vadjust
    width, height = self.drawable.get_size()
    gc.set_foreground(gtk.gdk.color_parse('light blue'))
    gc.set_line_attributes(2, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_MITER)
    while y < height:
      self.drawable.draw_line(gc, 0, y, width, y)
      y += line_height
    
  @classmethod
  def Register(self):
    """Register the class as a Gtk widget."""
    gobject.type_register(KeyTrainTextView)

  def SetBackground(self, red):
    if red:
      color = 'red'
    else:
      color = 'white'
    self.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
    self.queue_draw()

  def SetStyles(self):
    buf = self.get_buffer()
    buf.create_tag('bold', 
        weight= pango.WEIGHT_BOLD,
    #    background_stipple=stipple,
        stretch_set=True)

    buf.create_tag('faded',
        foreground='#CCC')
    
    self.err_tag = buf.create_tag('err',
        weight=pango.WEIGHT_BOLD,
        foreground='#C00')

  def IgnoreButton(self, widget, evt):
    return True  # prevent other handlers

  def IgnoreKeystrokes(self, widget, evt):
    self.ScrollNextLineVisible()
    return True

  def ScrollNextLineVisible(self):
    tb = self.get_buffer()
    pos = tb.get_iter_at_mark(tb.get_insert())
    #pos.forward_lines(1)
    self.scroll_to_iter(pos, 0.2)


def Main():
  KeyTrainTextView.Register()
  win = gtk.Window()
  win.resize(200, 406)
  win.connect('delete-event', gtk.main_quit)

  ktTextView = KeyTrainTextView()
  ktTextView.get_buffer().set_text('Bob is here. where are you? you here too? Oh I see you now, you are over there. Is this text long enough?')
  win.add(ktTextView)

  win.show_all()
  gtk.main()


if __name__ == '__main__':
  Main()
