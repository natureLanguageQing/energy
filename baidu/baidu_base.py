# -*- coding: utf-8 -*-
# 作者:             inspurer(月小水长)
# 创建时间:          2020/11/27 22:10
# 运行环境           Python3.6+
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)
# 文件备注信息       如果遇到打不开的情况，可以先在浏览器打开一下百度搜索引擎
import csv
import os
from datetime import datetime, timedelta
from random import randint
from time import sleep

import requests
from lxml import etree


def parseTime(unformatedTime):
    if '分钟' in unformatedTime:
        minute = unformatedTime[:unformatedTime.find('分钟')]
        minute = timedelta(minutes=int(minute))
        return (datetime.now() -
                minute).strftime('%Y-%m-%d %H:%M')
    elif '小时' in unformatedTime:
        hour = unformatedTime[:unformatedTime.find('小时')]
        hour = timedelta(hours=int(hour))
        return (datetime.now() -
                hour).strftime('%Y-%m-%d %H:%M')
    else:
        return unformatedTime


def dealHtml(html, out_dir):
    results = html.xpath('//div[@class="result-op c-container xpath-log new-pmd"]')

    saveData = []

    for result in results:
        title = result.xpath('.//h3/a')[0]
        title = title.xpath('string(.)').strip()

        summary = result.xpath('.//span[@class="c-font-normal c-color-text"]')[0]
        summary = summary.xpath('string(.)').strip()

        # ./ 是直接下级，.// 是直接/间接下级
        infos = result.xpath('.//div[@class="news-source"]')[0]
        source, dateTime = infos.xpath(".//span[last()-1]/text()")[0], \
                           infos.xpath(".//span[last()]/text()")[0]

        dateTime = parseTime(dateTime)

        print('标题', title)
        print('来源', source)
        print('时间', dateTime)
        print('概要', summary)
        print('\n')

        saveData.append({
            'title': title,
            'source': source,
            'time': dateTime,
            'summary': summary
        })
    with open(os.path.join(out_dir, fileName), 'a+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        for row in saveData:
            writer.writerow([row['title'], row['source'], row['time'], row['summary']])


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Referer': 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%B0%D9%B6%C8%D0%C2%CE%C5&fr=zhidao'
}

url = 'https://www.baidu.com/s'

params = {
    'ie': 'utf-8',
    'medium': 0,
    # rtt=4 按时间排序 rtt=1 按焦点排序
    'rtt': 1,
    'bsst': 1,
    'rsv_dl': 'news_t_sk',
    'cl': 2,
    'tn': 'news',
    'rsv_bp': 1,
    'oq': '',
    'rsv_btype': 't',
    'f': 8,
}


def doSpider(keyword, sort_by='focus', export_path=""):
    '''
    :param export_path: 导出地址
    :param keyword: 搜索关键词
    :param sort_by: 排序规则，可选：focus(按焦点排序），time(按时间排序），默认 focus
    :return:
    '''
    global fileName
    fileName = '{}.csv'.format(keyword)
    if not os.path.exists(export_path):
        os.mkdir(export_path)
    if not os.path.exists(fileName):
        with open(os.path.join(export_path, fileName), 'w+', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'source', 'time', 'summary'])

    params['wd'] = keyword
    if sort_by == 'time':
        params['rtt'] = 4

    response = requests.get(url=url, params=params, headers=headers)

    html = etree.HTML(response.text)

    dealHtml(html, export_path)

    for page in range(1, 10):
        print('第 {} 页\n\n'.format(page))
        headers['Referer'] = response.url
        params['pn'] = page * 10

        response = requests.get(url=url, headers=headers, params=params)

        html = etree.HTML(response.text)

        dealHtml(html, export_path)

        sleep(randint(2, 4))
    ...
