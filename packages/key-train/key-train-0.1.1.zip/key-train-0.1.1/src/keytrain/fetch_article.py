#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All rights reserved.

"""Fetch an article from Wikipedia.

It strips out most things so thtat its down to section titles, and paragraphs, mostly.
This could be useful for creating bigrams, trigrams for a language.
"""

__author__ = 'scott@forusers.com (Scott Kirkwood)'

import urllib2
from lxml import etree
import codecs
import re
import optparse


class ArticleInfo:
  def __init__(self, skip_sections):
    self._first_p = False
    self.quit = False
    self.sections = [['Top', [[]]]]
    self.title = ''
    if skip_sections:
      self.skip_sections = skip_sections
    else:
      self.skip_sections = ['See_also', 'References', 'Sister_cities', 'Notes']

  def title(self):
    return self.title

  def DumpYaml(self, fo):
    import yaml
    del self._first_p
    del self.quit
    yaml.dump(self, fo)

  def FetchArticle(self, lang, page_name):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = 'http://%s.wikipedia.org/w/index.php?title=%s&printable=yes' % (lang, page_name)
    print 'Fetching: %s' % url
    infile = opener.open(url)
    page = infile.read()
    self.url = url
    self.page = page_name
    self.lang = lang
    self._ParseText(page)
    self._Cleanup()

  def PrettyPrint(self, fo):
    fo.write('Title: %s\n' % self.title)
    for section, paragraphs in self.sections:
      fo.write('\n\n')
      fo.write('Section: %s\n' % section)
      fo.write('=========%s\n' % ('=' * len(section)))
      for paragraph in paragraphs:
        fo.write(''.join(paragraph))

  def _Cleanup(self):
    for section, paragraphs in self.sections:
      index = 0
      for paragraph in paragraphs[:]:
        txt = ''.join(paragraph)
        txt = txt.strip()
        if txt:
          paragraphs[index] = txt
          index += 1
        else:
          del paragraphs[index]

  def _ParseText(self, html):
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&reg;', '\uAE')
    tree = etree.fromstring(html)
    content = None
    for elem in tree.getiterator('{http://www.w3.org/1999/xhtml}div'):
      if 'id' in elem.attrib and elem.attrib['id'] == 'content':
        content = elem
        break
    if content is None:
      print 'Unable to find element'
      return None
    for a in content.getchildren():
      IterTag(a, self, self.skip_sections)
    if not self.sections[-1][0]:
      self.sections = self.sections[:-1]
    return self


def HasTagAttrib(a, tag, tagsearch, attribs):
  if tag != tagsearch:
    return False
  for key, values in attribs.items():
    if key not in a.attrib:
      return False
    for value in values:
      if value in a.attrib[key]:
        return True
  return False
  

def IterTag(a, pi, skip_sections):
  if pi.quit:
    return
  tag = str(a.tag).replace('{http://www.w3.org/1999/xhtml}', '')
  if HasTagAttrib(a, tag, 'h1', dict(id=['firstHeading'])) and a.text:
    pi.title = a.text
  if not pi._first_p:
    if tag == 'p':
      pi._first_p = True
    else:
      for x in a.getchildren():
        IterTag(x, pi, skip_sections)
      return
  if tag in ['table', 'li', 'td', 'th']:
    # Skip tables, lists
    return
  if tag == 'sup':
    # Skip references
    return
  if HasTagAttrib(a, tag, 'div', {'class': ['thumb']}):
    # Skip thumb images
    return
  if HasTagAttrib(a, tag, 'div', {'class': ['mainarticle', 'relarticle', 'rellink']}):
    # Skip pointers to other documents
    return
  if HasTagAttrib(a, tag, 'span', dict(id=skip_sections)):
    pi.quit = True
    return
  if tag == 'p':
    pi.sections[-1][1].append([])
  if tag in ['h2', 'h3', 'h4']:
    pi.sections.append(['', [[]]])
  elif a.text and tag not in ['script']:
    if not pi.sections[-1][0]:
      pi.sections[-1][0] = a.text
    else:
      pi.sections[-1][1][-1].append(CleanupText(a.text))
  for x in a.getchildren():
    IterTag(x, pi, skip_sections)
  if a.tail:
    pi.sections[-1][1][-1].append(CleanupText(a.tail))

def CleanupText(text):
  text = re.sub(u'\u2018|u2019', '\'', text)  # Normalize quote marks
  text = re.sub(u'\u201C|\u201D\u201F', '"', text)   # Normalize quotation marks
  text = re.sub(u'\u2010|\u2011|\u2012|\u2013|\u2014|\u2015', '-', text)  # Normalize hypehens
  return text

if __name__ == '__main__':
  desc = '%prog will fetch the article given by *link*. ex. "Albert_Einstein"'
  parser = optparse.OptionParser('%prog [options] link', description=desc)
  parser.add_option('-o', dest='outfile', default='article.txt',
      help='Name of the file to save the article.')
  parser.add_option('-l', dest='lang', default='en',
      help='Wikipedia Language (ex. en, pt) defaults to "%default"')
  options, args = parser.parse_args()
  if args:
    x = args[0]
  else:
    x = 'Knights_Templar'
  skip_sections = ['See_also', 'References', 'Sister_cities', 'Notes']
  ai = ArticleInfo(skip_sections)
  ai.FetchArticle(options.lang, x)

  fo = codecs.open(options.outfile, 'w', 'utf-8')
  ai.PrettyPrint(fo)
  fo.close()
  print 'Saved to %r' % options.outfile

  fo = codecs.open(options.outfile + '.yaml', 'w', 'utf-8')
  ai.DumpYaml(fo)
  fo.close()
  print 'Saved to %r.yaml' % options.outfile
  #print x.encode('utf-8', 'ignore')fo.write('\nPostamble: ' + self.
