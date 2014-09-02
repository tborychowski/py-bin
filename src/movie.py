#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import re
from colorama import init  # Fore, Style
from pyquery import PyQuery as pq
from tabulate import tabulate


def get_quality(name):
    qual = '?'
    if re.search(r'blu\-?(ray)?', name, flags=re.I): qual = 'BluRay'
    elif re.search('dvd(rip)?', name, flags=re.I): qual = 'DVDr'
    elif re.search('brrip', name, flags=re.I): qual = 'BR'
    elif re.search('hdrip', name, flags=re.I): qual = 'HD'
    elif re.search('dvdscrn?', name, flags=re.I): qual = 'DVDScr'
    elif re.search('r5', name, flags=re.I): qual = 'R5'
    elif re.search(r'web\-?(dl|rip)', name, flags=re.I): qual = 'Web'
    elif re.search('r6', name, flags=re.I): qual = 'R6'
    elif re.search('ts(rip)?', name, flags=re.I): qual = 'TS'
    elif re.search('cam(rip)?', name, flags=re.I): qual = 'Cam'
    return qual


def get_year(name):
    year = re.search(r'(19|20)(\d{2})', name)
    if year: return re.sub(r'.*(19|20)(\d{2}).*', r'\1\2', name)
    else: return '?'


def get_age(name):
    return re.sub(r'^(\d+)(.+)(d|h)(\w+s?)$', r'\1\3', name)


def clean_name(name):
    cln = [
        '\\w264', 'mp3', 'xvid', 'divx', 'aac', 'ac3', '~', '[\\s|-]rip', 'download', 'dubbed',
        'shift', 'h?dts', '\\sts', '\\smd', 'juggs', 'prisak', 'rajonboy', 'YIFY', 'tamil', 'hd',
        'team', 'mafiaking', 'hon3y', 'publichd', 'unrated', 'truefrench', 'rarbg', 'tomcat12',
        'maniacs', 'd3si', 'sample', 'torrent', 'art3mis', 'french', 'akatsuki', 'utt', 'ddhrg',
        '(\\d{3,4}p)', '(\\d+mb)', '([x|\\d]+cd)', '\\s\\d', 'brrip', 'dvd(scr(n)?)?(rip)?',
        'blu\\-?ray', 'bdrip', 'h3ll2p4y', 'italian', 't4p3', 'vision', 'venum', 'carpediem',
        '(e\\-)?subs', 'hellraz0r', 'jyk', 'mms', 'titan', 'k3ly', 'presents00', 'destroy', 'sap',
        'hc', 'rip', 'aqos', 'web', 'readnfo', 'subtitles', 'dus', 'BL4CKP34RL', 'ShAaNiG', 'tnt',
        'new( good)? source', 'v2', 'millenium', 'newsource', 'dd5', 'dl', 'english', 'svr',
        'web\\-?dl', '(br|hd)rip', 'hdcam(rip)?', 'r5', 'r6', 'cam', 'sumo', 'webrip', 'ntsc',
        'evo\\s', 'evo$', 'blitzcrieg', 'oo0oo'
    ]
    name = re.sub(r'\.', ' ', name)                           # dots to spaces
    name = re.sub(r'\(?(19|20)(\d{2})\)?', ' ', name)         # remove year
    for i in cln: name = re.sub(i, '', name, flags=re.I)      # remove words
    name = re.sub(r'\[.*\]', '', name)                        # brackets
    name = re.sub(r'\{.*\}', '', name)                        # curly braces
    name = re.sub(r'\(.*\)', '', name)                        # parents
    name = re.sub(r'\s?\-+\s?', ' ', name)                    # dashes
    name = re.sub(r'\s{2,}', ' ', name)                       # double spaces
    return name.strip()


def get_row(row):
    cells = pq(row).find('td')
    name = cells.find('.cellMainLink').text() if len(cells) else ''
    if not name: return
    if re.search('hindi|punjabi|indian|malay|raja', name, re.I): return
    quality = get_quality(name)
    year = get_year(name)
    age = get_age(cells.eq(3).text())
    name = clean_name(name)
    return [name, quality, year, age]


def get():
    site = pq('http://kickass.to')
    tab = site('#wrapperInner .mainpart .doublecelltable table').eq(0).find('tr')
    out = []
    for tabrow in tab.items():
        if tabrow.hasClass('firstr'): continue
        row = get_row(tabrow)
        if row: out.append(row)
    print (tabulate(out, ['Name', 'Rip', 'Year', 'Age'], tablefmt='simple'))


init(autoreset=True)
parser = argparse.ArgumentParser(prog='movie', description='KAT checker', version='1.0')
args = parser.parse_args()
get()
