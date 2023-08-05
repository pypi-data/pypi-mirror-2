#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Scott Kirkwood. All rights reserved.

__author__ = 'scott@forusers.com (Scott Kirkwood)'

from lxml import etree
import codecs
import keytrain.fetch_article as fetch_article
import gzip
import optparse
import os
import re
import sys
import traceback
import urllib
import urllib2

LANG2FEATURED = {
  'en': 'Wikipedia:Former_featured_articles',
  'pt': 'Wikipedia:Ex-artigos_destacados',
}
LANG2SKIPSEC = {
  'en': ['See_also', 'Bibliography', 'References', 'Notes', 'External_links', 
         'Further_reading', 'Sister_cities', ],
  'pt': ['Ver_tamb.C3.A9m', 'Refer.C3.AAncias', 'Notas', 'Refer.C3.AAncias_e_notas', 
         'Bibliografia', 'Cidades-irm.C3.A3s', 'Liga.C3.A7.C3.B5es_externas'],
}

class ManyArticles:
  def __init__(self):
    self.pathname = os.path.dirname(__file__)

  def Fetch(self, lang):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    self.lang = lang
    page_name = LANG2FEATURED[self.lang]
    url = 'http://%s.wikipedia.org/w/index.php?title=%s&printable=yes' % (lang, page_name)
    print 'Fetching: %s' % url
    infile = opener.open(url)
    html = infile.read()
    html = html.replace('&nbsp;', ' ').replace('&reg;', '(reg)')
    tree = etree.fromstring(html)
    self.GrabArticles(tree)

  def GrabArticles(self, tree):
    """Returns the list of article types followed by article names.
    Args:
      tree: The page.
    Returns:
      [['Title', ['article', 'article']], ['Title2', [...], ...]]
    """
    self.articles = []
    re_wiki = re.compile(r'/wiki/([^/]+)')
    for elem in tree.getiterator():
      tag = str(elem.tag)
      if tag.endswith('span'):
        if 'class' in elem.attrib and 'mw-headline' in elem.attrib['class']:
          self.articles.append([elem.text, []])
      elif tag.endswith('a'):
        if 'href' in elem.attrib:
          url = elem.attrib['href']
          grps = re_wiki.match(url)
          if grps:
            article = grps.group(1)
            if not self.BadArticle(article) and self.articles:
              self.articles[-1][1].append(article)

  def BadArticle(self, article):
    if ':' in article:
      return True
    if '.svg' in article:
      return True
    if '.png' in article:
      return True
    return False

  def StartFetching(self):
    for section, articles in self.articles:
      for article in articles:
        ai = fetch_article.ArticleInfo(LANG2SKIPSEC[self.lang])
        try:
          ai.FetchArticle(self.lang, article)
          sfname = urllib.pathname2url(section).replace('%20', '_')
        except Exception, e:
          print 'Unable to load %r: %s' % (article, e)
          traceback.print_exc(file=sys.stdout)
          continue
        dir = os.path.join(self.pathname, 'articles', self.lang, sfname)
        if not os.path.exists(dir):
          os.makedirs(dir)
        fname = os.path.join(dir, article + '.yaml.gz')
        #fo = codecs.open(fname, 'w', 'utf-8')
        fo = gzip.open(fname, 'wb')
        print 'Wrote %r' % fname
        ai.section = section
        ai.DumpYaml(fo)
        fo.close()


if __name__ == '__main__':
  import optparse
  parser = optparse.OptionParser()
  parser.add_option('-l', '--lang', dest='lang', default='en',
                    help='Start with language given (ex. pt_BR, en)')
  (options, args) = parser.parse_args()

  ma = ManyArticles()
  ma.Fetch(options.lang)
  ma.StartFetching()
