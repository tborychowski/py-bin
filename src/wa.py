#!/usr/bin/env python

import requests
import argparse
from bs4 import BeautifulSoup
from colorama import init, Fore


def is_additional(title):
    sections = [
        'Wikipedia', 'Corresponding', 'Comparison', 'Visual form',
        'Additional', 'Interpretations', 'American pronunciation',
        'Other notable uses', 'Notable books', 'map', 'plot',
        'Narrower terms', 'Broader terms', 'Translations', 'Word frequency',
        'Crossword puzzle', 'Scrabble', 'Rhymes', 'Anagrams', 'Hyphenation',
        'Exchange history', 'Frequency allocation', 'Electromagnetic frequency range'
    ]
    if title == 'Image' or title == 'Timeline': return True
    for s in sections:
        if title.find(s) > -1: return True
    return False


def get_definition(phrase):
    url = ('http://api.wolframalpha.com/v2/query?primary=true&appid=35EK93-QJX849VTRA'
           '&format=plaintext&input=' + phrase)

    resp = requests.get(url).text.encode('utf-8')
    xml = BeautifulSoup(resp)
    pods = xml.queryresult.find_all('pod')

    for pod in pods:
        if is_additional(pod['title']): continue
        if pod['title'] == 'Input interpretation':
            print(Fore.CYAN + 'WOLFRAM: ' + pod.subpod.plaintext.string + Fore.RESET)
            continue

        print(Fore.YELLOW + '\n' + pod['title'] + Fore.RESET)
        for sub in pod.find_all('subpod'):
            if not sub['title'] and not sub.plaintext: continue
            if sub['title']: sub['title'] = '(' + sub['title'] + ') '
            print (sub['title'] + (sub.plaintext.string or ''))


init()      # init colors on windows too

parser = argparse.ArgumentParser(prog='wa', description='Wolfram Alpha CLI', version='1.0')
parser.add_argument('phrase', help='text to search', nargs='+')
args = parser.parse_args()
if args.phrase: get_definition(' '.join(args.phrase))
