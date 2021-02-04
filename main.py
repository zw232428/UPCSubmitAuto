# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 10:26:25 2021
Author WarCock
"""

signIn = {'username': 'Z20160119', 'password': '190013'}
old_geo_api_info = {"type":"complete","info":"SUCCESS","status":1,"$Da":"jsonp_719041_","position":{"Q":21.66355,"R":109.15258,"lng":109.15258,"lat":21.66355},"message":"Get+geolocation+time+out.Get+ipLocation+success.Get+address+success.","location_type":"ip","accuracy":null,"isConverted":true,"addressComponent":{"citycode":"0779","adcode":"450521","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"兴江大道","streetNumber":"103乡","country":"中国","province":"广西壮族自治区","city":"北海市","district":"合浦县","township":"党江镇"},"formattedAddress":"广西壮族自治区北海市合浦县党江镇兴江大道","roads":[],"crosses":[],"pois":[]}

import requests
import json
import lxml.html
import re

conn = requests.Session()
signInResponse= conn.post(
    url="https://app.upc.edu.cn/uc/wap/login/check",
    data= signIn
)

historyResponse = conn.get(
    url="https://app.upc.edu.cn/ncov/wap/default/index?from=history",
    data={'from': 'history'}
)

html = lxml.html.fromstring(historyResponse.text)
JS = html.xpath('/html/body/script[@type="text/javascript"]')
JStr = JS[0].text
default = re.search('var def = {.*};',JStr).group()
oldInfo = re.search('oldInfo: {.*},',JStr).group()

firstParam = re.search('sfzgsxsx: .,',JStr).group()
firstParam = '"' + firstParam.replace(':','":')
secondParam = re.search('sfzhbsxsx: .,',JStr).group()
secondParam = '"' +  secondParam.replace(':','":')
lastParam = re.search('szgjcs: \'(.*)\'',JStr).group()
lastParam = lastParam.replace('szgjcs: \'','').rstrip('\'')

newInfo = oldInfo
newInfo = newInfo.replace('oldInfo: {','{' + firstParam + secondParam).rstrip(',')

defaultStrip = default.replace('var def = ','').rstrip(';')
defdic = json.loads(defaultStrip)

dic = json.loads(newInfo)
dic['ismoved'] = '0'
for j in ["date","created","id","gwszdd","sfyqjzgc","jrsfqzys","jrsfqzfy"]:
    dic[j] = defdic[j]
dic['szgjcs'] = lastParam
dic['geo_api_info'] = old_geo_api_info

saveResponse = conn.post(
    url="https://app.upc.edu.cn/ncov/wap/default/save",
    #headers=HEADERS,
    data = dic
)
