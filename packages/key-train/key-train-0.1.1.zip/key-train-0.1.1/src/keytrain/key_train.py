#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All Rights Reserved.

"""One-line documentation for key_train module.

A detailed description of key_train.
Gross Words Per Minute.
Total keystrokes in typing test / time

Normal Words per minute substracts 5 strokes for every error!
Net words per minute subtract 2 for each error.
Ex. 75 words in 3 minutes with 2 errors = (75 words/3 minutes)-(2 errors * 2) = 21 nwpm

nwpm also subtracts 1 for each error (standards, so many to choose from!)
"""

__author__ = 'scott@forusers.com (Scott Kirkwood)'
__version__ = '0.1.1'

import cairo
import gettext
import gobject
import gtk
import logging
import os
import pango
import pygtk
import sys
import time
import unicodedata

gettext.install('key-train', 'locale') 

import deadkeys
import image_backed_widget
import instructions_box
import keyboard_image
import keytrain_textview
import lazy_pixbuf_creator
import lessons
import my_dialog
import pretty_label
import scancodes

pygtk.require('2.0')


class KeyTrain():
  def __init__(self, options):
    self.debug = options.debug
    self.png = options.png
    self.pathname = os.path.dirname(__file__)

    self.name_fnames = {
      'kbd': [self.ImageName('keyboard')],
      'home': [self.ImageName('keyboard'), self.ImageName('images/home')],
      '18': [self.ImageName('keyboard'), self.ImageName('images/18')],  # e
      '23': [self.ImageName('keyboard'), self.ImageName('images/23')],  # i
      '34': [self.ImageName('keyboard'), self.ImageName('images/34')],  # g
      '35': [self.ImageName('keyboard'), self.ImageName('images/35')],  # h
    }
    self.scale = 1.0
    self.has_done_key = True
    self.pixbufs = lazy_pixbuf_creator.LazyPixbufCreator(self.name_fnames,
                                                         self.scale)
    self.langs = ['en', 'pt_BR']
    self.kbds = ['us', 'abtn']

    self.SetDefaultOptions()
    self.lang = self.langs[0]
    self.kbd = self.kbds[0]

    self.SetLanguage(options.lang)

    self.deadkey = deadkeys.DeadKey()

    self.scancodes = scancodes.ScanCodes()
    self.scancodes.ReadFile(os.path.join(self.pathname, '%s.kbd' % self.kbd))

    self.lessons = lessons.Lessons(self.lang, self.scancodes, self.debug)
    self.lessons.ReadLessons(self.pathname)

    self.ResetStats()

    pretty_label.PrettyLabel.Register()
    my_dialog.MyDialog.Register()
    image_backed_widget.ImageBackedWidget.Register()
    instructions_box.InstructionsBox.Register()

    self.CreateWindow()

  def ImageName(self, name):
    if self.png:
      return os.path.join(self.pathname, name + '.png')
    else:
      return os.path.join(self.pathname, name + '.svg')

  def SetDefaultOptions(self):
    self.allow_errs = True  # Can the user type errors and continue?
    self.ignore_accent = True  # Can the user enter a character with a missing accent?
    self.ignore_case = True  # Can the user type in the wrong case?
    self.ignore_whitespace = True  # Can the user skip typing white space?
    self.space_is_return = True  # Can a space be used by the return key?

  def CreateWindow(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    width, height = 800 * self.scale, 600 * self.scale
    self.window.set_default_size(int(width), int(height))
    self.window.set_title(_('Keyboard Trainer'))

    # Vbox for entire window
    self.vbox = gtk.VBox(homogeneous=False, spacing=0)
    self.window.add(self.vbox)

    dropdown_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.CreateDropdowns(dropdown_hbox)
    dropdown_hbox.show()
    self.vbox.pack_start(dropdown_hbox, expand=True, fill=True, padding=5)

    top_hbox = gtk.HBox(homogeneous=False, spacing=0)

    self.CreateTextBox(top_hbox)
    top_hbox.show()

    self.vbox.pack_start(top_hbox, expand=True, fill=True)
    
    self.bot_hbox = gtk.HBox(homogeneous=False, spacing=0)
    self.keyboard = keyboard_image.KeyboardImage(self.pixbufs, 'home')
    self.bot_hbox.pack_start(self.keyboard, expand=True, fill=False, padding=0)
    self.bot_hbox.show()
    self.vbox.pack_start(self.bot_hbox, expand=True, fill=True, padding=0)

    self.stats_hbox = gtk.HBox(homogeneous=False, spacing=0)

    vbox = gtk.VBox(homogeneous=False, spacing=0)
    self.CreateAccuracyBox(vbox)
    self.CreateWpmBox(vbox)
    self.stats_hbox.pack_start(vbox, expand=False, fill=False, padding=0)
    vbox.show()

    self.CreateOptionsBox(self.stats_hbox)

    vbox = gtk.VBox(homogeneous=False, spacing=0)
    self.CreateTimerBox(vbox)
    self.CreateCountDownBox(vbox)
    self.stats_hbox.pack_start(vbox, expand=False, fill=False, padding=0)
    vbox.show()

    self.stats_hbox.show()
    self.vbox.pack_start(self.stats_hbox, expand=False, fill=False, padding=0)

    self.CreateInstructionsBox(self.vbox)

    self.AddEvents()
    self.vbox.show()
    self.SetFocus()
    self.window.show()
    self.LessonUpdated()

  def NextLesson(self):
    self.lesson = self.lessons.NextLesson()
    self.LessonUpdated()

  def RepeatLesson(self):
    self.LessonUpdated()

  def LessonUpdated(self):
    self.lesson = self.lessons.CurLesson()
    self.lesson.SetOptions(self)
    self.SetText(self.lesson.lesson_text)
    self.level_dropdown.set_active(self.lessons.level_index)
    self.ShowInstructions()
    if self.lesson.new_keys:
      scancodes = [self.scancodes.CharToScanCodes(c)[0] for c in self.lesson.new_keys]
      self.keyboard.DrawScanCodes(scancodes, False)
      logging.info('Lesson updated')

  def CreateInstructionsBox(self, box):
    self.instructions = instructions_box.InstructionsBox()
    self.instructions.SetText(_('Will start when you start typing.'))
    self.instructions.set_size_request(-1, 100)
    box.pack_start(self.instructions, expand=True, fill=False, padding=10)
    self.instructions.show()

  def CreateWpmBox(self, box):
    self.wpm = pretty_label.PrettyLabel(self.ImageName('status'))
    self.wpm.set_width_chars(8)
    self.wpm.set_text(_('Speed 0 wpm'))
    self.wpm.set_tooltip_text(
        _('Your raw speed in words per minute. Ignores errors.'))
    box.pack_start(self.wpm, expand=True, fill=False, padding=0)
    self.wpm.show()

  def CreateTimerBox(self, box):
    self.timer = pretty_label.PrettyLabel(self.ImageName('status'))
    self.timer.set_width_chars(8)
    self.timer.set_text('0:00')
    self.timer.set_tooltip_text(
        _('Duration of lesson.'))
    box.pack_start(self.timer, expand=True, fill=False, padding=0)
    self.timer.show()
    gobject.timeout_add(1000, self.UpdateTimer)

  def CreateCountDownBox(self, box):
    self.countdown_timer = pretty_label.PrettyLabel(self.ImageName('status'))
    self.countdown_timer.set_width_chars(8)
    self.countdown_timer.set_text('60:00')
    self.countdown_timer.set_tooltip_text(
        _('Time limit for lesson.'))
    box.pack_start(self.countdown_timer, expand=True, fill=False, padding=0)
    self.countdown_timer.show()

  def CreateAccuracyBox(self, box):
    self.accuracy = pretty_label.PrettyLabel(self.ImageName('status'))
    self.accuracy.set_width_chars(4)
    self.accuracy.set_text(_('100% Accurate'))
    self.accuracy.set_tooltip_text(
        _('Number of error you have made as a percentate of text you have enetered so far.'))
    box.pack_start(self.accuracy, expand=True, fill=False, padding=0)
    self.accuracy.show()

  def CreateOptionsBox(self, box):
    self.options_box = image_backed_widget.ImageBackedWidget(self.ImageName('options'))
    self.options_box.set_flags(self.options_box.flags() & ~gtk.CAN_FOCUS)

    vbox = gtk.VBox(homogeneous=False, spacing=0)
    self.AddCheckButton('ignore_case', _('Ignore Case'), vbox,
       _('Ignore errors in upper or lower case'))
    self.AddCheckButton('ignore_accent', _('Ignore accent'), vbox,
       _('Ignore errors in accents'))
    self.AddCheckButton('ignore_whitespace', _('Ignore Whitespace'), vbox,
       _('Ignore errors of extra or missing spacebar'))
    self.options_box.pack_start(vbox, expand=True, fill=True)
    vbox.show()

    vbox = gtk.VBox(homogeneous=False, spacing=0)
    self.AddCheckButton('allow_errs', _('Allow Errors'), vbox,
        _('Errors can be enters and must be corrected before continuing.'))
    self.options_box.pack_start(vbox, expand=True, fill=True)
    vbox.show()

    self.options_box.show()
    box.pack_start(self.options_box, expand=True, fill=False, padding=0)

  def AddCheckButton(self, name, desc, box, tooltip):
    check_name = name + '_check'
    setattr(self, check_name, gtk.CheckButton(desc))
    button = getattr(self, check_name)
    button.show()
    button.set_property('focus-on-click', False)
    button.set_property('can-focus', False) 
    button.set_active(getattr(self, name))
    button.set_tooltip_text(tooltip)
    box.pack_start(button, expand=False, fill=False)
    button.connect('clicked', self.CheckButtonClicked, name)

  def CheckButtonClicked(self, button, name):
    value = button.get_active()
    setattr(self, name, value)

  def CreateDropdowns(self, box):
    self.lang_dropdown = self.AddDropdown(_('Language'), [
        _('English'), _('Portuguese')], 0, box)
    self.lang_dropdown.connect('changed', self.LanguageChanged)
    self.kbd_dropdown = self.AddDropdown(_('Keyboard'), [
        _('US'), _('ABTN (Brazilian)')], 0, box)
    self.kbd_dropdown.connect('changed', self.KeyboardChanged)
    self.lesson_dropdown = self.AddDropdown(_('Lesson'), [
        _('Beginner'), _('Practice')], 0, box)
    self.lesson_dropdown.connect('changed', self.LessonChanged)
    self.level_dropdown = self.AddDropdown(_('Level'), range(1, self.lessons.NumLevels() + 1), 0, box)
    self.level_dropdown.connect('changed', self.LevelChanged)
   
  def AddDropdown(self, label, strings, active_index, box):
    lb = gtk.Label()
    lb.set_text(label + ':')
    lb.show()
    box.pack_start(lb, expand=False, fill=False, padding=10)

    liststore = gtk.ListStore(gobject.TYPE_STRING)
    for string in strings:
      liststore.append([string])
    combo = gtk.ComboBox(liststore)
    cell = gtk.CellRendererText()
    combo.pack_start(cell, True)
    combo.add_attribute(cell, 'text', 0)
    combo.set_flags(combo.flags() & ~gtk.CAN_FOCUS)
    combo.set_property('can-focus', False)
    combo.set_property('can-default', False)
    combo.set_property('focus-on-click', False)
    combo.show()
    box.pack_start(combo, expand=False, fill=False)
    combo.set_active(active_index)
    return combo
    
  def LanguageChanged(self, combo):
    new = combo.get_active()
    self.lang = self.langs[new]
    logging.info('Language changed to %r' % self.lang)
    self.lessons = lessons.Lessons(self.lang, self.debug)

    self.lessons.ReadLessons(self.pathname)
    self.ResetStats()
    self.LessonUpdated()

  def SetLanguage(self, lang):
    if not lang:
      return
    if lang not in self.langs:
      print 'Option %r not a known language' % lang
      return
    self.lang = lang
    lang = gettext.translation('key-train', os.path.join(self.pathname, 'locale'), languages=[self.lang])
    logging.info('Switching to language %s' % self.lang)
    lang.install(unicode=True)
    logging.info('This should say "Lesson" (%r) in the appropriate language' % _('Lesson'))

  def KeyboardChanged(self, combo):
    new = combo.get_active()
    logging.info('Keyboard changed to %d' % new)

  def LessonChanged(self, combo):
    new = combo.get_active()
    logging.info('Lesson changed to %d' % new)
    self.lessons.SetLesson(new, 0) 
    liststore = self.level_dropdown.get_model()
    liststore.clear()
    for n in range(1, self.lessons.NumLevels() + 1):
      liststore.append([str(n)])
    self.level_dropdown.set_active(0)
    self.LessonUpdated()

  def LevelChanged(self, combo):
    new = combo.get_active()
    logging.info('Level changed to %d' % new)
    self.lessons.SetLesson(self.lessons.lesson_index, new)
    self.LessonUpdated()

  def CreateTextBox(self, box):
    scrolled_window = gtk.ScrolledWindow()
    scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    scrolled_window.set_border_width(10)
    scrolled_window.show()

    self.text_view = keytrain_textview.KeyTrainTextView()
    self.text_buffer = self.text_view.get_buffer()

    # This set the vertical size of the text view.
    self.text_view.set_size_request(-1, 150)

    self.text_view.show()
    scrolled_window.add(self.text_view)
    pad = 1
    box.pack_start(scrolled_window, expand=True, fill=True, padding=pad)

  def SetText(self, text):
    tb = self.text_buffer
    tb.set_text(text)
    self.cur_lesson_text = text
    tb.place_cursor(tb.get_start_iter())
    tb.apply_tag_by_name('bold', tb.get_start_iter(), tb.get_end_iter())
    self.ResetStats()

  def ResetStats(self):
    self.total_err_count = 0  # Every error encountered
    self.cur_err_count = 0  # Uncorrected errors currently
    self.total_corrected_errors = 0  # Errors come in bursts, this lowers the error count
    self.training_start_time = None
    self.training_end_time = None
    self.failed = False

  def AcceptText(self, count):
    tb = self.text_buffer
    old_pos = tb.get_iter_at_mark(tb.get_insert())
    new_pos = old_pos.copy()
    for i in range(count):
      new_pos.forward_char()
    tb.apply_tag_by_name('faded', old_pos, new_pos)
    tb.place_cursor(new_pos)

  def AcceptChar(self, char):
    """Should we accept the char entered by user?"""
    if self.cur_err_count:
      return False
    text = self.GetNextChar()
    if text == '\n':
      text = '\r'
    if text == char:
      self.AcceptText(1)
      return True
    if char.isspace() and text == '\r' and self.space_is_return:
      self.AcceptText(1)
      return True
    if self.ignore_case and char.lower() == text.lower():
      self.AcceptText(1)
      return True
    if self.ignore_accent and char == self.Unaccent(text):
      self.AcceptText(1)
      return True
    if self.ignore_whitespace and text.isspace():
      next_2_char = self.GetNextChar(2)[-1]
      if next_2_char == char or (self.ignore_case and next_2_char.lower() ==
                                 char.lower()):
        self.AcceptText(2)
        return True
    return False

  def Unaccent(self, text):
    # replace accented characters with non-accented ones
    if isinstance(text, str):
      return text
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

  def IsDone(self):
    if self.training_end_time:
      return True
    tb = self.text_buffer
    cur_pos = tb.get_iter_at_mark(tb.get_insert())
    if cur_pos.is_end():
      return True
    return False

  def HasFailed(self):
    if self.CalculateAccuracy() < self.lesson.min_accuracy:
      return True
    return self.failed

  def HandleBackspace(self):
    """If permitted, backspace over an error."""
    tb = self.text_buffer
    pos = tb.get_iter_at_mark(tb.get_insert())
    back_pos = pos.copy()
    back_pos.backward_char()
    if back_pos.has_tag(self.text_view.err_tag):
      self.cur_err_count -= 1
      tb.delete(back_pos, pos)
      if self.cur_err_count == 0:
        self.total_corrected_errors += 1
        self.text_view.SetBackground(False)

  def GetNextChar(self, dir=1):
    """Gets the following text from the cursor position.
    Args:
      dir: the direction, maybe > 1
    Returns:
      The next character or characters, or the previous characters if dir
      is negative.
    """
    tb = self.text_buffer
    start_pos = tb.get_iter_at_mark(tb.get_insert())
    next_pos = start_pos.copy()
    if dir > 0:
      next_pos.forward_chars(dir)
    elif dir < 0:
      next_pos.backward_chars(-dir)
    text = tb.get_text(start_pos, next_pos, include_hidden_chars=False)
    return text

  def AddError(self, char):
    self.total_err_count += 1
    self.FlashError()
    
    if not self.allow_errs:
      return False
    tb = self.text_buffer
    if char == ' ':
      char = u'\u2423'  # Visible space
    elif char == '\r':
      return False  # completely ignore the enter key
    tb.insert_at_cursor(char)
    self.cur_err_count += 1
    end_pos = tb.get_iter_at_mark(tb.get_insert())
    begin_pos = end_pos.copy()
    begin_pos.backward_char()
    tb.apply_tag_by_name('err', begin_pos, end_pos)

    return True

  def FlashError(self):
    self.text_view.SetBackground(True)
    if not self.allow_errs:
      gobject.timeout_add(200, self.RevertBackground)
      
  def RevertBackground(self):
    """For the red flash effect"""
    self.text_view.SetBackground(False)
  
  #TODO(scott): These Key related methods should go in a keyboard class.
  def IsBackspaceKey(self, scancode):
    if self.allow_errs and scancode == 14:
      return True
    return False

  def IsCursorKey(self, keyval):
    if keyval in [gtk.keysyms.Right, gtk.keysyms.Left, gtk.keysyms.Down, gtk.keysyms.Up,
       gtk.keysyms.Home, gtk.keysyms.End, gtk.keysyms.Page_Up, gtk.keysyms.Page_Down,
       gtk.keysyms.KP_Right, gtk.keysyms.KP_Left, gtk.keysyms.KP_Down, gtk.keysyms.KP_Up,
       gtk.keysyms.KP_Home, gtk.keysyms.KP_End, gtk.keysyms.KP_Page_Down, gtk.keysyms.KP_Page_Up]:
      return True
    return False

  def AddEvents(self):
    self.window.connect('destroy', self.Destroy)
    self.window.connect('key_press_event', self.KeyDown)
    self.window.connect('key_release_event', self.KeyUp)

    accelgroup = gtk.AccelGroup()
    key, modifier = gtk.accelerator_parse('<Control>q')
    accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, self.Quit)
    self.window.add_accel_group(accelgroup)

  def IsShiftKey(self, scancode):
    if scancode in [29, 42, 54, 56, 58, 69, 70, 84, 97, 100, 125, 126, 127]:
      return True
    return False

  def KeyDown(self, widget, data):
    scancode = scancodes.ToMyScanCode(data.hardware_keycode)
    logging.info('HW keycode %d, scancode %d' % (data.hardware_keycode, scancode))
    if self.has_done_key and (scancode == 107 or scancode == 95):  # END key
      logging.info('Hit done key')
      self.ShowStats()
    if self.deadkey.WasDeadKey(data.keyval):
      logging.info('IsDeadKey')
      return
    if self.IsCursorKey(data.keyval):
      logging.info('IsCursorKey')
      return
    txt = self.deadkey.ConvertText(data.string)
    text = self.GetNextChar()
    for code in self.scancodes.CharToScanCodes(text):
      self.keyboard.DrawScanCode(code, False)
    if self.AcceptChar(txt):
      self.SetWpm(self.CalculateWpm())
      self.SetAccuracy(self.CalculateAccuracy())
    elif self.IsBackspaceKey(scancode):
      self.HandleBackspace()
    elif not self.IsShiftKey(scancode):
      if data.state & gtk.gdk.LOCK_MASK:
        self.keyboard.CapslockWarning()
      self.AddError(txt)
      self.SetAccuracy(self.CalculateAccuracy())
    if self.IsDone():
      self.training_end_time = time.time()
      self.ShowStats()

  def ShowStats(self):
    postamble_last = self.lesson.postamble_text
    raw_wpm = _('%0.f words per minute') % self.CalculateWpm()
    accuracy_percent = _('%.0f%% accurate') % self.CalculateAccuracy()
    net_wpm = _('%.0f net words per minute') % self.CalculateNetWpm()
    if self.HasFailed():
      text = _('Sorry, you will need to repeat this lesson.\n')
      if self.CalculateAccuracy() < self.lesson.min_accuracy:
        text += _('You did not meet the minimum accuracy of %d%%\n') % self.lesson.min_accuracy
      if self.CalculateWpm() <= self.lesson.min_wpm:
        text += _('You did not meet the minimum typing speed of %d wpm') % self.lesson.min_wpm
    else:
      preamble_new = self.lesson.preamble_text
      text = postamble_last + '\n' + preamble_new
    replace = {
        'text': text,
        'raw_wpm': raw_wpm,
        'accuracy_percent': accuracy_percent,
        'net_wpm': net_wpm }
    dialog = my_dialog.MyDialog(
        self.ImageName('finished'),
        'Finished', None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE),
        replace)
    dialog.show_all()
    dialog.run()
    dialog.destroy()
    if self.HasFailed():
      self.RepeatLesson()
    else:
      self.NextLesson()

  def ShowInstructions(self):
    if not self.lesson.instructions_text:
      return
    self.instructions.SetText(self.lesson.instructions_text)

  def SetFocus(self):
    self.window.grab_focus()
    self.text_view.grab_focus()
    
  def SetWpm(self, wpm):
    self.wpm.set_text(_('Speed %3.0f wpm') % wpm)

  def SetAccuracy(self, accuracy):
    self.accuracy.set_text(_('%3.0f%% Accurate') % accuracy)

  def UpdateTimer(self):
    if self.training_start_time and self.training_end_time:
      delta = self.training_end_time - self.training_start_time
    elif self.training_start_time:
      delta = time.time() - self.training_start_time
    else:
      delta = 0
    min = delta / 60
    sec = delta % 60
    self.timer.set_text('%2d:%02d' % (min, sec))
    
    if self.lesson.min_wpm:
      left = ((60 * len(self.cur_lesson_text)) / self.lesson.min_wpm) - delta
    min = left / 60
    sec = left % 60
    self.countdown_timer.set_text('%2d:%02d' % (min, sec))
    if min < 0 and not self.training_end_time:
      self.failed = True
      self.training_end_time = time.time()
    return True   # Keep firing the timer

  def CalculateWpm(self):
    if self.training_start_time is None:
      self.training_start_time = time.time()
      return 0.0
    tb = self.text_buffer
    chars_entered = tb.get_iter_at_mark(tb.get_insert()).get_offset()
    if chars_entered == 0:
      return 0.0
    delta_time_secs = time.time() - self.training_start_time
    return 60.0 * (float(chars_entered) / 5) / delta_time_secs

  def CalculateNetWpm(self):
    tb = self.text_buffer
    chars_entered = tb.get_iter_at_mark(tb.get_insert()).get_offset()
    if chars_entered == 0:
      return 0.0
    delta_time_secs = time.time() - self.training_start_time
    fudge = 1.0
    return 60.0 * (float(chars_entered) / 5) / delta_time_secs - (fudge * self.total_corrected_errors)

  def CalculateAccuracy(self):
    tb = self.text_buffer
    chars_entered = tb.get_iter_at_mark(tb.get_insert()).get_offset()
    if chars_entered == 0:
      return 100.0
    ret = 100.0 - ((100.0 * self.total_err_count) / chars_entered)
    if ret < 0.0:
      return 0.0
    return ret

  def KeyUp(self, evt, data):
    self.keyboard.KeyUp(data.hardware_keycode)

  def Quit(self, *args):
    self.Destroy(None)

  def Destroy(self, widget, data=None):
    gtk.main_quit()


def Main():
  import optparse
  parser = optparse.OptionParser()
  parser.add_option('-d', '--debug', dest='debug', action='store_true',
                    help='Output debugging information.')
  parser.add_option('-p', '--png', dest='png', action='store_true',
                    help='Use png files instead of svg files')
  parser.add_option('-l', '--lang', dest='lang',
                    help='Start with language given (ex. pt_BR, en)')
  (options, args) = parser.parse_args()
  if options.debug:
    logging.basicConfig(level=logging.DEBUG, format = "%(filename)s [%(lineno)d]: %(levelname)s %(message)s")
  key_train = KeyTrain(options)
  gtk.main()

if __name__ == "__main__":
  Main()
