#encoding= utf-8
import urllib, urllib2
import cookielib
import re
import time
import pyDatabase.mySql as mySql
from bs4 import BeautifulSoup#放在lib里面

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'
headers = {'User-Agent':'Chrome/28.0.1468.0 Safari/537.36','Referer':'','Content-Type':'application/x-www-form-urlencoded'}
class weiboCNParser(object):
    def __init__(self, username, pwd ,validDate):
        self.username = username
        self.pwd = pwd
        self.validDate = validDate
        # Add cookies:
        #获取一个保存cookie的对象
        cj = cookielib.LWPCookieJar()
        #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        #创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        #将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
        urllib2.install_opener(opener)    
        
        url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
        rand, passwd, vk = self.get_rand(url)
        data = urllib.urlencode({'mobile': self.username,
                                  passwd: self.pwd,
                                 'remember': 'on',
                                 'backURL': 'http://weibo.cn/',
                                 'backTitle': '新浪微博',
                                 'vk': vk,
                                 'submit': '登录',
                                 'encoding': 'utf-8'})
        url = 'http://3g.sina.com.cn/prog/wapsite/sso/' + rand   
        req = urllib2.Request(url, data, headers)
        resp = urllib2.urlopen(req)
        html1 = resp.read()
        cookie = cj.extract_cookies(resp,req)
        soup = BeautifulSoup(html1)
        go = soup.find_all('go')
        jumpUrl = go[0].get('href')
        request = urllib2.Request(jumpUrl)
        request.add_header('User-agent', user_agent)
        response = urllib2.urlopen(request)
    
    def weiboCNContentParser(self,uids):
        contentsDict = {}
        for uid in uids:
            url = 'http://weibo.cn/%s/profile?filter=1' %uid
            contents = []
            contents,soup,valid = self.getPageContent(url,contents)
            if not valid:
                continue
            # get total page num
            totalPage = self.getPageNum(soup)
            # next page
            pageNum = 2
            while pageNum < totalPage:          
                pageUrl = 'http://weibo.cn/%s/profile?page=%d' %(uid,pageNum)
                contents,soup,valid = self.getPageContent(pageUrl,contents)
                if not valid:
                    break
                pageNum = pageNum + 1
                time.sleep(5)      
            print 'contents:'
            print str(contents)
            contentsDict[uid] = contents
        return contentsDict
        
    def weiboCNContentFilter(self,keyword,startDate,endDate,uid):
        contentsDict = {}
        data = urllib.urlencode({
                'advancedfilter': 0,
                'endtime':endDate,
                'hasori':1,
                'haspic':0,
                'keyword':keyword,
                'smblog':'筛选',
                'starttime':startDate,
                'uid':uid
            })
        url = 'http://weibo.cn/%s/profile?filter=1' %uid
        contents = []
        contents,soup,valid = self.getPageContent(url,contents)
        # get total page num
        totalPage = self.getPageNum(soup)
        if valid:
            #   next page
            pageNum = 2
            #urllib2.quote('#')
            while pageNum < totalPage:          
                pageUrl = 'http://weibo.cn/%s/profile?keyword=%s&hasori=1&haspic=0&starttime=%d&endtime=%d&advancedfilter=0&page=%d' %(uid,keyword,startDate,endDate,pageNum)
                contents,soup,valid = self.getPageContent(pageUrl,contents)
                if not valid:
                    break
                pageNum = pageNum + 1
                time.sleep(5)              
        contentsDict[uid] = contents
        return contentsDict    
            
    def getPageContent(self,pageUrl,contents):
        request = urllib2.Request(pageUrl)
        request.set_proxy('192.168.8.87:3128','http')
        request.add_header('User-agent', user_agent)
        response = urllib2.urlopen(request)
        html = response.read()
        soup  = BeautifulSoup(html)
        divs = soup.find_all('div',attrs={"class":"c"})
        i = 0
        valid = True
        while i < len(divs) - 2:
            content = []
            div_soup = BeautifulSoup(str(divs[i].div))
            span1 = div_soup.find('span',attrs={"class":"ctt"})
            span2 = div_soup.find('span',attrs={"class":"ct"})
            if span2 == None:
                i = i + 1
                continue
            if self.dateValid(span2.get_text().encode('utf-8')):    
                a_tags = div_soup.find_all('a')
                string = ''
                for a_tag in a_tags:
                    string = string + a_tag.get_text().encode('utf-8')
                zan,zhuanfa,pinglun = self.extractNum(string)
                content.append(span1.get_text().encode('utf-8'))
                content.append(zan)
                content.append(zhuanfa)
                content.append(pinglun)
                i = i + 1
                contents = list(contents)
                contents.append(content)
                valid = True
            else:
                valid = False
                break 
        return contents,soup,valid
    
    def DBOperation(self):
        # Database
        pass
        """
        print "Writing to the database:"
        sqlDB_test = mySql.sqlDB()
        sqlDB_test.createTable('ParserResult')
        sqlDB_test.writeDataToDB(contentsDict,'ParserResult')
        """
        
    def get_rand(self,url):   
        req = urllib2.Request(url ,urllib.urlencode({}), headers)
        resp = urllib2.urlopen(req)
        login_page = resp.read()
        soup = BeautifulSoup(login_page)
        go = soup.findAll('go')[0]
        rand = go.get('href')

        postfield = go.findAll('postfield')
        passwd_elem = postfield[1]
        passwd = passwd_elem.get('name')
        vk_elem = postfield[2]
        vk = vk_elem.get('value')
    
        return rand, passwd, vk
    
    def extractNum(self, string):
        pattern = re.compile(r'\[\d{1,10}\]')
        results = re.findall(pattern,string)
        zan = results[0][1:(len(results[0])-1)]
        zhuanfa = results[1][1:(len(results[0])-1)]
        pinglun = results[2][1:(len(results[0])-1)]
        print zan,zhuanfa,pinglun
        return zan,zhuanfa,pinglun
    
    def dateValid(self, info):
        if '今天' in info:
            return True
        elif '月' in info:
            pattern = re.compile(r'\d{2}')
            results = re.findall(pattern,info)
            date = int(results[0]*30) + int(results[1]) + 2013*12*30
        else:
            pattern1 = re.compile(r'\d{4}')
            year = int(re.findall(pattern1,info)[0])
            pattern2 = re.compile(r'-\d{2}')
            results = re.findall(pattern2,info)
            date = year*12*30 + int(results[0][1:])*30 + int(results[1][1:])
        if date < self.validDate:
            return False
        else:
            return True
    
    def getPageNum(self, soup):
        div = soup.find_all(attrs={"id":"pagelist"})
        page_text = div[0].form.div.get_text().encode('utf-8')
        pattern = re.compile(r'\/\d{1,2}')
        match = re.findall(pattern,page_text)
        totalPage = int(match[0][1:])
        return totalPage