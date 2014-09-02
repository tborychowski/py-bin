#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
from colorama import init, Fore, Style


def print_header(src, tar, phrase, s):
    print (Style.DIM + (s['src_translit'] or src) + ' ' +
           Style.NORMAL + phrase + ' -> ' +
           Style.DIM + tar + ' ' +
           Fore.CYAN + Style.BRIGHT + s['trans'])


def print_dict(phrase, s):
    print(phrase + ' ' + Style.DIM + s['pos'] + Style.NORMAL + ' ' + ', '.join(s['terms']))


def format_response(src, tar, phrase, json):
    if 'sentences' in json:
        for s in json['sentences']: print_header(src, tar, phrase, s)

    if 'dict' in json:
        print('')
        for s in json['dict']: print_dict(phrase, s)


def translate(src, tar, phrase):
    url = ('http://translate.google.com/translate_a/t?client=p&hl=en&sc=2&ie=UTF-8&oe=UTF-8&oc=1'
           '&otf=1&ssel=0&tsel=0&sl=' + src + '&psl=' + tar + '&tl=' + tar + '&uptl=' +
           tar + '&q=' + phrase)

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    format_response(src, tar, phrase, resp.json())


init(autoreset=True)      # init colors on windows too

parser = argparse.ArgumentParser(prog='ling', description='Google Translator', version='1.0')
parser.add_argument('src', help='source language')
parser.add_argument('tar', help='target language')
parser.add_argument('phrase', help='text to translate', nargs='+')
args = parser.parse_args()

if args.phrase: translate(args.src, args.tar, ' '.join(args.phrase))
