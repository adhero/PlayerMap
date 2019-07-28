# usr/bin/env python3;
#-*-coding: utf-8-*-

import pandas as pd
import numpy as np
import json
import re
import os

def has_integrated():
    try:
        dirpath = 'geoplayer/leagues'
        filelist = os.listdir('geoplayer/leagues')
        with open("geoplayer/players_data.csv", "w", encoding="gbk") as f:
            for item in filelist:
                for txt in open(os.path.join(dirpath,item), "r"):
                    f.write(txt)
    except Exception as e:
        print(e)
    return True

def flush_data():
    header = ['name', 'link', 'height', 'weight', 'nation', 'birth', 'position']
    data = pd.read_csv('players_data.csv', encoding='gbk', header=None)
    data.columns = header
    data.head(5)
    target = data.loc[:,['name','nation']]
    target.dropna(inplace=True)    
    # 读取国家中英文对照表
    with open('geoplayer/nations.json') as f:
        nations = json.loads(f.read())    # json文件的输出参数indent和ensure_ascii使json文件便于阅读
    target = target.replace({'Cura?ao': '荷兰', 'England': 'United Kingdom'})     # 特殊符号，特殊国家
    target['nation'] = target['nation'].map(lambda x:nations[x] if need_convert(x) else x)
    target = target.replace('', np.nan)
    target.dropna(inplace=True)
    attr = target['nation'].value_counts().index.tolist()
    value = target['nation'].value_counts().values.tolist()
    return attr, value

def is_zh(zh):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    return zhPattern.search(zh)

def need_convert(x):
    if not str(x).encode('utf-8').isalpha() and len(str(x).split())==1:
        return True
    else:
        #print(x)   # 输出源数据为英文的国家名
        return False

#flush_data()