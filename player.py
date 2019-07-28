#!usr/bin/env python3
#-*-coding: utf-8-*-
'''
目标：通过football-data.org的API获取五大联赛所有球员的国籍信息，然后通过第三方软件库绘制世界分布图。
一、获取数据
1.建立五大competition（联赛）字典
2.遍历competition值，存入teams字典
3.遍历teams，获取所有球员信息，存为csv文件
二、绘制分布图
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import csv
from multiprocessing.pool import Pool


def save_data(data, league):
    filename = "playermap/leagues/{}.csv".format(league)
    with open(filename, 'a', encoding='gbk') as f:
        fieldnames = ['p_name', 'p_link', 'height', 'weight', 'nation', 'birth', 'pos']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)
        
def main(league):
    base_url = 'https://soccer.stats.qq.com/table.htm?type='
    url = base_url + league
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    link_list = browser.find_elements(By.XPATH, '//a[@class="tname"]')
    club_list = browser.find_elements(By.XPATH, '//a[@class="tname"]/span')
    zipped = zip(link_list, club_list)
    dic = {}
    # 存入俱乐部信息字典
    for link, club in zipped:
        c_link = link.get_attribute('href')
        c_name = club.text
        dic[c_name] = {'c_link': c_link}
    
    for club in dic.keys():
        p_url = dic[club]['c_link']
        browser.get(p_url)
        player_elements = browser.find_elements(By.XPATH,'//ul[@class="player-list"]//a')
        player_list = []
        # 遍历球员链接
        for player in player_elements:
            p_name = player.get_attribute('title')
            p_link = player.get_attribute('href')
            # get player info
            players_handle = browser.current_window_handle
            browser.execute_script('window.open()')
            browser.switch_to_window(browser.window_handles[1])
            browser.get(p_link)
            info_list = browser.find_elements(By.XPATH, '//ul[@class="item-list"]/li')
            info = [inf.text for inf in info_list]
            # 读取球员信息
            parse_text = lambda x: x.split('：')[1]
            height = parse_text(info[1])
            weight = parse_text(info[2])
            nation = parse_text(info[3])
            birth = parse_text(info[4])
            pos = parse_text(info[5])
            # 存入球员信息字典
            player_info = {'p_name': p_name,
                                 'p_link': p_link,
                                 'height': height,
                                 'weight': weight,
                                 'nation': nation,
                                 'birth': birth,
                                 'pos': pos}
            player_list.append(player_info)
            # 返回俱乐部选项卡
            browser.close()
            browser.switch_to_window(players_handle)
            save_data(player_info, league)
        dic[club]['player_list'] = player_list
        print(club + " is done.")
    browser.close()
    return dic

if __name__ == '__main__':
    start = time.clock()
    leagues = ['yingchao', 'xijia', 'dejia', 'yijia', 'fajia']
    '''
    for url in urls:
        main(url)
    '''
    p = Pool()
    p.map(main, leagues)
    p.close()
    p.join()
    elapsed = (time.clock() - start)
    print("Time used: ", elapsed)
