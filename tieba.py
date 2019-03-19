from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from xlutils.copy import copy
import urllib.request
import re
import xlwt
import xlrd
import sys
import os
import operator

urlDict = {}


def urlSpider(url):  # url爬虫的具体功能实现
    total = 0
    haveNext = 1
    print("开始爬取页面url导入url管理器")
    while haveNext == 1:
        if (total > 10):
            return 0
        total += 1
        webSource = urlopen(url)
        file = open("urls.txt", 'a', encoding='utf-8')
        html = webSource.read().decode('utf-8')
        bsObj = BeautifulSoup(html)
        for x in bsObj.find_all("div", class_="threadlist_lz clearfix"):
            # for x in bsObj.find_all(href=re.compile("/p/")):
            allEle = x.find(href=re.compile("/p/"))
            newTitle = allEle.get('title')
            newTitle = newTitle.translate(str.maketrans('', '', '\\/:*?"<>|.'))
            print(newTitle)
            newUrl = "https://tieba.baidu.com" + allEle.get('href')
            file.write(newUrl)
            print(newUrl)
            author = x.find("span", class_="tb_icon_author ")
            newAuthor = author.get('title')
            urlDict[newTitle] = [str(newUrl), str(newAuthor)]
        isHaveNext = bsObj.find("a", class_="next pagination-item ")
        if isHaveNext:
            url = "https:" + isHaveNext.get('href')
            print(url)
        else:
            print("链接爬取已完成")
            haveNext = 0


def urlManager(needuser):  # 要去爬取的url的管理器
    print("进入URL管理程序>>>")
    wb = xlrd.open_workbook("urlList.xls")
    mysheet = wb.sheet_by_name("MyUrl")
    for x in range(mysheet.nrows):
        thisName = mysheet.cell(x, 0).value
        thisUser = mysheet.cell(x, 1).value
        thisUrl = mysheet.cell(x, 2).value
        if (thisName.strip() != ''):
            if (operator.eq(needuser, "0")):
                articleSpider(thisUrl, thisName)
            else:
                if (needuser in thisUser):
                    articleSpider(thisUrl, thisName)


def pageEdit(pageContent):
    bs = BeautifulSoup(pageContent)
    pageContent = bs.find("div", class_="left_section")
    htmlHead = "<html>" + str(bs.head) + "<body>"
    htmlFoot = "</body>" + "</html>"
    htmlTotal = str(htmlHead) + str(pageContent) + str(htmlFoot)
    return htmlTotal


def articleSpider(url, thisName):  # 爬虫的具体功能实现
    print("开始爬取制定的某一帖子")
    print(url + ":" + thisName)
    # 拼接文件夹名称并消除名称中末尾的点符,用以避免错误
    dirname = "download\\" + thisName
    print(dir)
    os.mkdir(dirname)
    isHaveNext = 0
    i = 1
    thisurl = url
    while isHaveNext != -1:
        thispage = urlopen(thisurl)
        pageContent = thispage.read().decode('utf-8')
        pageFileName = "download\\" + thisName.strip('.') + "\\" + str(i) + ".html"
        htmlFile = open(pageFileName, 'w', encoding='utf-8')
        pageContent = pageEdit(pageContent)
        htmlFile.write(str(pageContent))
        isHaveNext = pageContent.find("下一页")
        if (isHaveNext != -1):
            i = i + 1
            thisurl = url + "?pn=" + str(i)


def clearExcal():
    wb = xlwt.Workbook('urlList.xls')
    worksheet = wb.add_sheet('MyUrl')
    wb.save('urlList.xls')
    print("清理完成")


def interface():  # 交互界面
    while 1:
        print("0.退出程序")
        print("1.爬取指定贴吧帖子地址url列表存入exacl")
        print("2.爬取exacl中所存全部帖子的内容")
        print("3.爬取exacl中制定人的帖子内容")
        print("4.清空exacl表格中所存URL列表")
        select = int(input("请输入指令序号"))
        if (select == 1):
            print("请输入要爬取的贴吧名称:")
            tbName = str(input())
            thisUrl = "https://tieba.baidu.com/f?kw=" + urllib.parse.quote(tbName) + "&ie=utf-8"
            print("当前贴吧首页链接:" + thisUrl)
            urlSpider(thisUrl)
            urlSave()
        elif (select == 2):
            print("进入贴子内容下载程序...")
            urlManager("0")
        elif (select == 3):
            username = input("请输入所要爬取用户名")
            urlManager(username)
        elif (select == 4):
            clearExcal()
        elif (select == 0):
            return 0


def urlSave():
    wb = xlrd.open_workbook('urlList.xls')
    newb = copy(wb)
    sumsheet = newb.get_sheet('MyUrl')
    k = len(sumsheet.rows)
    for x in urlDict.keys():
        sumsheet.write(k, 0, x)
        sumsheet.write(k, 1, urlDict[x][1][6:])
        sumsheet.write(k, 2, urlDict[x][0])
        sumsheet.write(k, 3, 0)
        k += 1
    newb.save('urlList.xls')


if __name__ == '__main__':
    interface()
