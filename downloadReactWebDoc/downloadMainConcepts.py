#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 02:48:49 2019

@author: apple
"""

import requests
import re
from bs4 import BeautifulSoup
import time



# 取得 html 網頁原始碼
def crawl(url, htmlEncoding, sleepTime=0):
    headers = {'User-Agent': 'Mozilla/5.0'}
    html = requests.get(url, headers=headers)
    time.sleep(sleepTime);
    html.encoding = htmlEncoding    #解決簡體中文亂碼問題
    return BeautifulSoup(html.text, 'html.parser')

 

# 過濾自己會的單字
def filterWord(wordDict, filterFilePath, filterFileName):
    print('過濾單字...')
    openFilePath = filterFilePath
    openFileName = filterFileName
    fr = open(openFilePath + openFileName, 'r', encoding='UTF-8')
    openString = fr.read()
    filterList = openString.split(',\n')
    
    print('原本有',len(wordDict),'個詞彙')
    for word in wordDict.copy():
        if word in filterList:
            wordDict.pop(word, None)
    wordDict.pop('', None)
    print('過濾後總共有',len(wordDict),'個詞彙')
    return wordDict


    
# 利用 voicetube.com 的翻譯網站實作英翻中程式
def translateWordByVoiceTube(word):
    print("'" + word + "'", 'translating...')
    url = 'https://tw.voicetube.com/definition/' + word    
    soup = crawl(url, 'utf-8', 3)
    pageArticle = soup.find_all('div', {'id': 'definition'})
    
    if len(pageArticle) != 0:
        splitTranslate = (pageArticle[0].get_text()).split('例句')
        #print(splitTranslate[0])
        return splitTranslate[0].lstrip().strip('解釋')
    else:
        return 'none'


try:
    print('爬取資料...')
    url = 'https://reactjs.org/docs/hello-world.html'
    soup = crawl(url, 'utf-8')
    pageArticle = soup.find_all('article', {'class': 'css-174qq1k'})   
    articleHeader = soup.find_all('h1', {'class': 'css-1rwyxsf'})   
    articleH2 = pageArticle[0].find_all('h2')   
    articleUlLi = pageArticle[0].find_all('ul')
    articleOlLi = pageArticle[0].find_all('ol')
    articleContent = pageArticle[0].find_all('p')
    
    clearTagContent = ''
    outputContent = ''
    
    # 擷取 <h1></h1>
    clearTagContent += articleHeader[0].get_text() + ' '
    
    # 擷取 <h2></h2>
    for h2string in articleH2:
        #print(str(i), h2string.get_text() , '\n\n')
        clearTagContent += h2string.get_text() + ' '
    
    # 擷取 <ul></ul
    if len(articleUlLi) != 0:
        clearTagContent += articleUlLi[0].get_text() + ' '
    
    # 擷取 <ol></ol>
    if len(articleOlLi) != 0:
        clearTagContent += articleOlLi[0].get_text() + ' '
        
    # 擷取 <p></p>
    for content in articleContent:
        clearTagContent += content.get_text()
        
        '''
        # html 的標籤正則表達式
        regEx = re.findall("<[^>]+>", str(content))
        #print(regEx)
        
        # 如果 <p></p> 含有文字以外的標籤，利用正則表達式把裡面的標籤濾掉
        if str(type(content.string)) == "<class 'NoneType'>":
            for replaceStr in regEx:        
                content = str(content).replace(replaceStr, '')
            #clearTagContent += content
        else:
            i = 0
            #clearTagContent += content.string
        '''
        
    #print(clearTagContent)
    print('整理資料...')
    # 利用正則表達式把不必要的標點符號刪除
    clearTagContent = re.sub('[0-9!\"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~\n，。！：（）；€【】「❤éфриендыл？”“、～]', ' ', clearTagContent)
    listContent = clearTagContent.split(' ')
    outputDict = {}
    
    # 先以單字做排序，並加以統計單字出現次數（文字雲的概念）
    for outputWord in sorted(listContent):
        if outputWord not in outputDict.keys():
            outputDict.update({outputWord:1})
            
        else:
            outputDict[outputWord] += 1
    
    openFilePath = './'
    openFileName = '過濾簡單的單字.txt'
    outputDict = filterWord(outputDict, openFilePath, openFileName)
    
    
    print('匯出資料...')
    filePath = './'
    fileName = '2 - Introducing JSX'
    # 以出現平率最高的單字排序
    for word in sorted(outputDict, key=outputDict.get, reverse=True):    
        fw = open(filePath + fileName + '.txt', 'a', encoding='UTF-8')
        fw.write(word + ', ' + str(outputDict[word]) + ', \r\n')
        explanation = translateWordByVoiceTube(word);
        if explanation != 'none':
            fw.write(explanation + '\r\r')
        else:
            fw.write('\r\r')
        fw.close()
    print('完成')
    
except Exception as ex:
    print(str(ex))
    


