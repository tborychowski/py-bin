#!/usr/bin/env python
import imaplib
import re


def check():
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        imap.login('', '')
        res = imap.status('INBOX', '(UNSEEN)')[1][0]
        print int(re.search(r'UNSEEN\s+(\d+)', res).group(1))
    except:
        print 'Check credentials'

check()
