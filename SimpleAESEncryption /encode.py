#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:41:24 2019

@author: apple
"""

from urllib import parse
from Crypto.Cipher import AES
import base64
import glob

try:
    # 讀取金鑰(16碼)
    openKey = open('./key.txt', 'r')
    key = openKey.read()
    openKey.close()

    # 讀取要加密的位置
    openEncryptionPath = open('./Encryption path.txt', 'r')
    directoryPath = openEncryptionPath.read()
    openEncryptionPath.close()

    # 讀取要加密的檔案
    path = directoryPath + '/want encode file/*.txt'
    readPaths = glob.glob(path)
    chunk = 3
    secret_key = key
    
    for readPath in readPaths:
          
        splitPath = readPath.split('/')
        fileName = splitPath[-1]
        fileName = fileName.rstrip('.txt')
        readFile = open(readPath, 'r', encoding='utf-8')
        
        # 開始加密
        while True:
            readString = readFile.read(chunk)
            
            if not readString:
                break
            
            quoteStr = parse.quote(readString)  #將中文轉碼
            cipher = AES.new(secret_key, AES.MODE_ECB) # never use ECB in strong systems obviously
            encoded = base64.b64encode(cipher.encrypt(quoteStr.rjust(32)))
            
            fw = open(directoryPath + '/export file/' + fileName + ' - encoded.txt', 'ab')
            fw.write(encoded)
            fw.close()
            
        readFile.close()
        print('加密完成')
except Exception as ex:
    print('加密失敗')
    print('錯誤訊息:\n' + str(ex))

