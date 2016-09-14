# coding: utf-8

import requests
import re
from wox import Wox, WoxAPI
import webbrowser

"""
API from https://zhuanlan.zhihu.com/p/22421123?utm_source=tuicool&utm_medium=referral
"""

EMPTY_RESULT = {
    'Title': 'Start to find words',
    'SubTitle': 'Powered by bing',
    'IcoPath': 'Img\\youdao.ico'
}

NOT_RESULT = {
    'Title': 'Start to find words',
    'SubTitle': 'Powered by change',
    'IcoPath': 'Img\\youdao.ico'
}


class Main(Wox):

    def query1(self, query):
        results = []
        if query.strip() == '':
            results.append(EMPTY_RESULT)
        else:
            results.append({
                "Title": "Hello World",
                "SubTitle": "Query: {}".format(query.strip()),
                "IcoPath": "Images/app.ico"
            })
        return results

    def query(self, key):
        results = []
        if key.strip() == '':
            results.append(EMPTY_RESULT)
        else:
            url = "http://dict.cn/" + key
            results.append({
                "Title": "{}".format("打开网页查询" + key.strip()),
                "SubTitle": "{}".format(url.strip()),
                "IcoPath": "Images/app.ico",
                "JsonRPCAction": {
                    # 这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
                    "method": "openUrl",
                    # 参数必须以数组的形式传过去
                    "parameters": [url],
                    # 是否隐藏窗口
                    "dontHideAfterAction": True
                }
            })
            # res = self.dict_find(key.strip())
            res = self.word_find(key.strip())
            for line in res:
                results.append({
                    "Title": "{}".format(key.strip()),
                    # "SubTitle": "{}".format(line[0] + " " + line[1]),
                    "SubTitle": "{}".format(line['pos'] + " " + line['def']),
                    "IcoPath": "Images/app.ico"
                })
        return results

    def dict_find(self, key):
        res = 'nothing'
        origin = "http://dict.cn/"
        dict_ = key
        url = origin + dict_

        header = {'user-agent': 'mozilla/5.0'}
        response = requests.get(url, header)
        # print response.getcode()
        html_doc = response.text
        # f = open("d:/test.txt", 'w', encoding="utf8")
        # print(html_doc)
        # test = """<ul class=\"dict-basic-ul\">
        # aaaa</ul>sfsaaasddassdasda</ul>"""

        fd = re.search(
            r"<(ul) class=\"dict-basic-ul\">[\s\S]*?</\1>", html_doc)
        if fd == None:
            fd = re.search(
                r"<div class=\"basic clearfix\">[\s\S]*?</ul>", html_doc)
            fd = re.search(r"<(li)>[\s\S]*?</\1>\s+<li s", fd.group())
            res = re.findall(
                "<span>(.+)</span><strong>(.+)</strong>", fd.group())
        else:
            fd = re.search(r"<(li)>[\s\S]*?</\1>\s+<li s", fd.group())
            res = re.findall(
                "<span>(.+)</span><strong>(.+)</strong>", fd.group())
        # f.write(str(res))

        return res
        # print('get all links')
        # for line in res:
        #     print(line[0] + " " + line[1])

    def word_find(self, word):
        url = 'http://xtk.azurewebsites.net/BingDictService.aspx'
        datas = {'Word': word}
        # with open('d:/test.txt', 'w', encoding='utf8') as f:
        #     f.write(word)
        response = requests.get(url, params=datas)
        res = response.json()
        return res['defs']

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Main()
