#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 20:47:57 2019

@author: apple
"""

from urllib import parse
from Crypto.Cipher import AES
import base64
import glob
#import os


#print(os.getcwd())
#print(os.path.abspath('.'))
try:
    # 讀取金鑰(16碼)
    openKey = open('./key.txt', 'r')
    key = openKey.read()
    openKey.close()
    
    # 讀取要解密的位置
    openEncryptionPath = open('./Encryption path.txt', 'r')
    directoryPath = openEncryptionPath.read()
    openEncryptionPath.close()
    
    # 讀取要解密的檔案
    path = directoryPath + '/want decode file/*.txt'
    readPaths = glob.glob(path)
    chunk = 44
    secret_key = key
    
    for readPath in readPaths:
        splitPath = readPath.split('/')
        fileName = splitPath[-1]
        fileName = fileName.rstrip('.txt')
        readFile = open(readPath, 'r', encoding='utf-8')
        fileData = b''
        
        # 開始解密
        while True:
            readString = readFile.read(chunk)
            if not readString:
                break
            
            cipher = AES.new(secret_key, AES.MODE_ECB) # never use ECB in strong systems obviously
            decoded = cipher.decrypt(base64.b64decode(readString))
            fileData += decoded.strip()
            
        readFile.close()
        
        #將中文轉碼
        unquoteStr = parse.unquote(str(fileData))
        byteStr = bytes(unquoteStr, encoding='utf-8')
        byteStr = byteStr[2:-1]
        
        fw = open(directoryPath + '/export file/' + fileName + ' - decoded.txt', 'wb')
        fw.write(byteStr)
        fw.close()
        print('解密完成')
except Exception as ex:
    print('解密失敗')
    print('錯誤訊息:\n' + str(ex))


    
    
