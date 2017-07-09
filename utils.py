#!/usr/bin/python
#-*- coding:utf-8 -*-
'''
Created on 2017/6/26
@author: Bee
'''

import requests
from urllib.parse import urlparse

def get_owner_and_repo(url):
    parsed = urlparse(url)
    if parsed.netloc == 'github.com':
        path = parsed.path.split('/')
        if len(path) == 3:
            return path[1:]
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    print(get_owner_and_repo('https://github.com/rapid7/metasploit-framework'))