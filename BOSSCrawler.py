# -*- coding: utf-8 -*-
import json
import urllib
from requests import request
import re
import openpyxl
from openpyxl.workbook import Workbook
import time
from bs4 import BeautifulSoup

class boss_crawler:
    def __init__(self):
        self.headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,br',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connecion':'keep-alive',
                #'Cookie':'__a=32544699.1550979725.1550979725.1550979732.57.2.56.57; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1550979723,1552831132,1552906964; lastCity=101010100; _uab_collina=155283113440544880091396; __g=-; __l=r=&l=%2Fsao.zhipin.com%2F; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1552907207; __c=1550979732; JSESSIONID=""',
                'Host':'www.zhipin.com',
                'Referer':'https://www.zhipin.com/c101010100/',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
               }  # cookie会失效的，需要定期更换
        self.keyword = ['java']
        self.outwb = Workbook()

    def getHtml(self,url):
        time.sleep(2)
        response = request('get',url,headers=self.headers)
        #html = json.loads(response.text)
        html = response.text
        return html

    def getExcel(self,careerName):
        wo = self.outwb.active
        careerSheet = self.outwb.create_sheet(careerName)
        careerSheet.append(['公司','规模低', '规模顶','职位','最低工作经验','学历', '底薪', '顶薪', '发布时间'])
        return careerSheet

    def saveExcel(self):
        self.outwb.save("E:\DataAnalysis\\tools\python3\project\money_analysis\JodFinding\work.xlsx")

    def getNum(self,str):
        pattern = re.compile(r'\d+')
        result = pattern.findall(str)
        return result

    def getSchool(self,str):
        p = re.compile(r'[年]+')
        p_ = re.compile(r'[限]+')
        p__ = re.compile(r'[生]+')
        list1 = p.split(str)
        list2 = p_.split(str)
        list3 = p__.split(str)
        if len(list1)>1:
            print(list1)
            return list1[1]
        elif len(list2)>1:
            print(list2)
            return list2[1]
        else:
            try:
                print(list3)
                return list3[1]
            except:
                print('error')

    def get_SaveMessage(self,careerSheet,soup):
        joblist = soup.find_all('div', {'class': 'job-primary'})
        for item in joblist:
            company = item.find('div', {'class': 'info-company'}).find('a').get_text()
            big = item.find('div', {'class': 'info-company'}).find('p').get_text()
            job = item.find('div', {'class': 'info-primary'}).find('div', {'class': 'job-title'}).get_text()
            graduate = item.find('div', {'class': 'info-primary'}).p.get_text()
            money = item.find('div', {'class': 'info-primary'}).find('span').get_text()
            time = item.find('div', {'class': 'info-publis'}).find('p').get_text()
            if len(self.getNum(big))> 1:
                if len(self.getNum(graduate))>0:
                    careerSheet.append([company, self.getNum(big)[0],self.getNum(big)[1],job,self.getNum(graduate)[0],self.getSchool(graduate),self.getNum(money)[0],self.getNum(money)[1],time])
                else:
                    careerSheet.append([company, self.getNum(big)[0],self.getNum(big)[1],job,'无',self.getSchool(graduate),self.getNum(money)[0],self.getNum(money)[1],time])
            else:
                if len(self.getNum(graduate))>0:
                    careerSheet.append([company, self.getNum(big)[0],'以上',job,self.getNum(graduate)[0],self.getSchool(graduate),self.getNum(money)[0],self.getNum(money)[1], time])
                else:
                    careerSheet.append([company, self.getNum(big)[0],'以上',job,'无',self.getSchool(graduate),self.getNum(money)[0],self.getNum(money)[1],time])


    def startCrawl(self):
        for i in range(len(self.keyword)):  #按关键字进行爬取
            page = 0
            careerSheet = self.getExcel(self.keyword[i])
            url = 'https://www.zhipin.com/c101010100/?query=%s&page=%d&ka=page-%d' % (self.keyword[i], page, page) #&period=3 是近7天招聘的意思
            soup = BeautifulSoup(self.getHtml(url), 'lxml')
            self.get_SaveMessage(careerSheet,soup)
            while soup.find('a',{'class':'next'}): #如果有下一页
                if soup.find('a',{'class':'next disabled'}):
                    break
                page = page+1
                url = 'https://www.zhipin.com/c101010100/?query=%s&page=%d&ka=page-%d' % (self.keyword[i], page, page)
                soup = BeautifulSoup(self.getHtml(url), 'lxml')
                self.get_SaveMessage(careerSheet, soup)
            print(self.keyword[i] + 'is OK')
        self.saveExcel()

bs = boss_crawler()
bs.startCrawl()