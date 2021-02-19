import os
import requests
import json
import lxml.html
import re

signIn = {'username': os.environ["USERNAME"], #学号
          'password': os.environ["PASSWORD"]} #登陆密码

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; M2002J9E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.120 Mobile Safari/537.36',
}

conn = requests.Session()
signInResponse= conn.post(
    url="https://app.upc.edu.cn/uc/wap/login/check",
    headers=headers,
    data= signIn, 
    timeout=10
)

historyResponse = conn.get(
    url="https://app.upc.edu.cn/ncov/wap/default/index?from=history",
    headers=headers,
    data={'from': 'history'},
    timeout=10
)
historyResponse.encoding = "UTF-8"

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

saveResponse = conn.post(
    url="https://app.upc.edu.cn/ncov/wap/default/save",
    headers=headers,
    data = dic,
    timeout=10
)

SCKEY = "SCT9114TelDEIWEKRH6LrCQrUacIeE8A"
data = {"text": f"{username}的疫情防疫", "desp": "Github Action执行完成"}
requests.post(f"https://sctapi.ftqq.com/{SCKEY}.send", data={"疫情防疫": "Github Action执行完成"})

saveJson = json.loads(saveResponse.text)
print(saveJson['m'])
