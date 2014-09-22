#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import requests
from pyquery import PyQuery as pq
from lxml import etree

__version__ = '1.0'


def remove_attrs(el):
    attrs_to_remove = [ 'data-expanded-url', 'data-pre-embedded', 'data-query-source',
                        'dir', 'rel', 'nofollow', 'class', 'title', 'target' ]
    for a in attrs_to_remove:
        if (el.attr(a)): el.removeAttr(a)
    return el


def clean_links(el):
    ats = el.find('a.twitter-atreply,a.twitter-hashtag')
    for i, at in enumerate(ats):
        at = ats.eq(i)
        at.attr.href = 'https://twitter.com' + at.attr.href
        at = remove_attrs(at)
        at.html(at.text())

    ats = el.find('a.twitter-timeline-link')
    for i, at in enumerate(ats):
        at = ats.eq(i)
        lnk = at.find('.js-display-url')
        if lnk: at.html(lnk.text())
        else: at.html(at.text())
        if (at.attr('data-expanded-url')): at.attr.href = at.attr('data-expanded-url')
        at = remove_attrs(at)
    return el.html()


def read():
    resp = requests.get('https://twitter.com/xwerx')
    resp.encoding = 'utf-8'
    site = pq(resp.text, parser='html')
    tweets = site('.GridTimeline .GridTimeline-items .js-stream-item .js-tweet .js-tweet-text')
    for i, tweet in enumerate(tweets):
        if i > 4: break         # limit to 4 most recent tweets
        twt = tweets.eq(i)      # get pquery elem
        twt = clean_links(twt)
        print(twt + '\n')


parser = argparse.ArgumentParser(prog='twitter-reader', description='Twitter scraper')
parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))
args = parser.parse_args()
read()
