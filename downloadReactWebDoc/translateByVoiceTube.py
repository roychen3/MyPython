#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 21:32:17 2019

@author: apple
"""

import requests
from bs4 import BeautifulSoup



def translateWord(word):
    url = 'https://tw.voicetube.com/definition/' + word
    headers = {'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'    #解決簡體中文亂碼問題
    soup2 = BeautifulSoup(html.text, 'html.parser')
    pageArticle = soup2.find_all('div', {'id': 'definition'})
    
    if len(pageArticle) != 0:
        splitTranslate = (pageArticle[0].get_text()).split('例句')
        return splitTranslate[0].strip().lstrip('解釋')
    else:
        return 'none'
    
print('利用 voicetube.com 的翻譯網站實作英翻中程式')
print('請輸入英文單字：')
keydwon = input()
while keydwon != 'out()':
    print(translateWord(keydwon))
    keydwon = input()