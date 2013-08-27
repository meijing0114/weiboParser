#encoding= utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import xlrd
import xlwt


class webDriver(object):
    def __init__(self, urlDict, startPage,validDay,username,pwd,startKey ):  
        self.driver = webdriver.Firefox()
        self.username = username
        self.pwd = pwd
        self.urlDict = urlDict
        self.startPage = startPage
        self.validDay = validDay
        self.startKey = startKey
        self.weiboDict = {}
        try:
            self.logIn(startPage)
        except Exception:
            print "Login Problem"
            pass
            
    
    def logIn(self,startPage):
        self.driver.get(self.startPage)
        logIn = self.driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/p/a[2]')#登录
        logIn.click()
        time.sleep(5)
        username = self.driver.find_element_by_xpath('/html/body/div[12]/div/table/tbody/tr/td/div/div[2]/div/dl/form/dd/input') # 需要重构
        password = self.driver.find_element_by_xpath('/html/body/div[12]/div/table/tbody/tr/td/div/div[2]/div/dl/form/dd[2]/input')
        log = self.driver.find_element_by_xpath('/html/body/div[12]/div/table/tbody/tr/td/div/div[2]/div/dl/form/dd[3]/a/span')
        username.send_keys(self.username)
        password.send_keys(self.pwd)
        log.click()
    

    def getTime(self,date):
        weiboTime = 0
        pattern = re.compile(r'今天')
        match = re.findall(pattern,date)
        if match:
            structT = time.localtime(time.time())
            year = int(time.strftime('%Y',structT))
            month = int(time.strftime('%m',structT))
            day = int(time.strftime('%d',structT))
        else:
            pattern = re.compile(r'-\d{1,2}')
            match = re.findall(pattern,date)
            month = match[0]
            month = month[1:]
            month = int(month)
            day = match[1]
            day = day[1:]
            day = int(day)
            year = date[0:4]
            year = int(year)
        
        weiboTime = year*12*30 + month*30 + day
        return weiboTime
    
    
    def getWeiboDict(self,weiboDict,contents,Type,key,validDay):
        if Type == "professional":
            if weiboDict.has_key(key):
                infos = weiboDict[key]
            else:
                infos = []
            print "Prof:"+str(key)
            weiboTime = 0
            contents = contents.find_element_by_xpath("div[@class='feed_lists']")
            dls = contents.find_elements_by_tag_name('dl')
            for dl in dls:
                # strang thing: empty string comes out of nowhere
                info = []
                if dl.text !="":
                    className = dl.get_attribute('class')
                    if className != "feed_list W_linecolor ": #居然有一个空格
                        continue
                    content = dl.find_element_by_xpath("dd[@class='content']")
                    paragraph1 = content.find_element_by_xpath("p[@node-type='feed_list_content']")
                    p1 = paragraph1.text.encode('utf-8')
                    info.append(p1)
                    paragraph2 = content.find_element_by_xpath("p[@class='info W_linkb W_textb']")
                    date_elem = paragraph2.find_element_by_xpath("a[@class='date']")
                    appendix = date_elem.get_attribute('href')
                    weiboUrl = appendix;
                    info.append(weiboUrl)
                    date = date_elem.get_attribute('title')
                    pattern = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
                    match = re.findall(pattern,date)
                    info.append(match[0])
                    info.append(p1)
                    # if weibo is older than two monthes, then drop them.
                    weiboTime = self.getTime(date)
                    if weiboTime < validDay:
                        break
                    infos.append(info)
            weiboDict[key] = infos
        else:
            print "normal"+str(key)
            if weiboDict.has_key(key):
                infos = weiboDict[key]
            else:
                infos = []
            weiboTime = 0
            contents = contents.find_element_by_xpath("div[@class='PRF_modwrap clearfix']")
            contents = contents.find_element_by_xpath("div[@class='WB_feed WB_feed_self']")
            divs = contents.find_elements_by_xpath("div[@action-type='feed_list_item']")
            for div in divs:
                info = []
                if div.text != "":
                    content = div.find_element_by_xpath("div[@class='WB_feed_datail S_line2 clearfix']")
                    content = content.find_element_by_xpath("div[@class='WB_detail']")
                    text1 = content.find_element_by_xpath("div[@class='WB_text']")
                    p1 = text1.text.encode('utf-8')
                    info.append(p1)
                    text2 = content.find_element_by_xpath("div[@class='WB_func clearfix']")
                    text2 = text2.find_element_by_xpath("div[@class='WB_from']")
                    date_elem = text2.find_element_by_xpath("a[@class='S_link2 WB_time']")
                    appendix = date_elem.get_attribute('href')
                    weiboUrl = appendix;
                    info.append(weiboUrl)
                    date = date_elem.get_attribute('title')
                    pattern = re.compile(r'\d{4}-\d{1,2}-\d{1,2}')
                    match = re.findall(pattern,date)
                    info.append(match[0])
                    info.append(p1)
                    weiboTime = self.getTime(date)
                    if weiboTime < validDay:
                        break
                    infos.append(info)
            weiboDict[key] = infos
        self.weiboDict = weiboDict
        return weiboTime
    
    
    def webDrive(self):
        time.sleep(5)
        original = self.driver.find_element_by_link_text('原创') # 原创
        original.click()
        self.scrollMaster(self.driver)
        
        ID = 'pl_content_hisFeed'
        contents = self.driver.find_element_by_id(ID)
        url = self.driver.current_url
        weiboTime = self.getWeiboDict(self.weiboDict,contents,"professional",self.startKey,self.validDay)
        while(weiboTime >= self.validDay):
            time.sleep(7)
            nextPage = self.driver.find_element_by_link_text("下一页")
            nextPage.click()
            self.scrollMaster(self.driver)
            weiboTime = self.getWeiboDict(self.weiboDict,contents,"professional",self.startKey,self.validDay)
            
        # visit every other page the get all the information
        shopIDs = self.urlDict.keys()
        for shopID in shopIDs:
            url = self.urlDict[shopID]
            key = shopID
            url = url + "?type=0"
            self.driver.get(url)      
            currentURL = self.driver.current_url
            pattern = re.compile(r'.*e.weibo.*')
            match = pattern.match(currentURL)
            if match:
                # 专业版
                time.sleep(5)
                try:
                    mainPage = self.driver.find_element_by_link_text('主页')
                    mainPage.click()
                    time.sleep(7)
                    original = self.driver.find_element_by_link_text('原创') # 
                    original.click()
                    self.scrollMaster(self.driver)
                
                    ID = 'pl_content_hisFeed'
                    contents = self.driver.find_element_by_id(ID)
                except Exception:
                    print "mainpage original or scroll or id for prof "
                    pass
                try:    
                    weiboTime = self.getWeiboDict(self.weiboDict,contents,"professional",key,self.validDay)
                except Exception:
                    print "getWeiboDict prof "
                    pass
                while(weiboTime >= self.validDay):
                    time.sleep(5)
                    try:
                        #code
                        nextPage = self.driver.find_element_by_link_text("下一页")
                        nextPage.click()
                        self.scrollMaster(self.driver)
                        weiboTime = self.getWeiboDict(self.weiboDict,contents,"professional",key,self.validDay)
                    except Exception:
                        print "next page prof"
                        pass
                    
            else:
                # 个人版
                try:
                    time.sleep(10)
                    original = self.driver.find_element_by_link_text('原创') # 原创
                    original.click()
                    self.scrollMaster(self.driver)
                    ID = 'Pl_Official_LeftProfileFeed__10'
                    contents = self.driver.find_element_by_id(ID)
                    weiboTime = self.getWeiboDict(self.weiboDict,contents,"normal",key,self.validDay)
                except Exception:
                    print "mainpage original or scroll or id for normal "
                    pass
                
                while(weiboTime >= self.validDay):
                    try:
                        time.sleep(5)
                        nextPage = self.driver.find_element_by_link_text("下一页")
                        nextPage.click()
                        self.scrollMaster(self.driver)
                        weiboTime = self.getWeiboDict(self.weiboDict,contents,"normal",key,self.validDay)
                    except Exception:
                        print "nextpage normal"
                        pass
                    
                      
        return self.weiboDict
    
    def scrollMaster(self,driver):
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    

    
    
   
    