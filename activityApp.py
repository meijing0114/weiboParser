#encoding= utf-8
import pyDatabase.mySql as mySql
import utils.utils as utils
import weibo.weiboCNParser as weiboCNParser
import time

def main():
    structT = time.localtime(time.time())
    currentYear = int(time.strftime('%Y',structT))
    currentMonth = int(time.strftime('%m',structT))
    currentDay = int(time.strftime('%d',structT))
 
    username = raw_input('Please input username: ')
    pwd = raw_input('Please input weibo Password: ')
    day = int(raw_input('How many days of weibo do you neeed? '))
    outPath = raw_input('Input file name to save the results:')   
    proxy_ip = raw_input('Please input the proxy ip:')
    proxy_port = raw_input('Please input the proxy port:')
    proxy = proxy_ip + ':' + proxy_port
    parse = raw_input('Do you want to parse filtered results or normal ?F or N').lower()
    
    # Create an weiboCNParser instance and start parsing
    print "Start parsing...\n"
    validDay = currentYear*12*30 + currentMonth*30 + currentDay - day
    weiboParser = weiboCNParser.weiboCNParser(username, pwd,validDay,proxy)
    if parse =='N':
        weiboIDs = raw_input('Input weiboID(number or string) that you want to parse, split by "," : ')
        weiboIDs = weiboIDs.split(',') 
        contentsDict = weiboParser.weiboCNContentParser(weiboIDs)
    elif parse == 'F':
        startDate = int(raw_input('Input start date,eg: 20130812 :'))
        endDate = int(raw_input('Input end date,eg: 20130812 :'))
        keyword = raw_input('Input keyword')
        uid = raw_input('Input uid:')
        contentsDict = weiboParser.weiboCNContentFilter(keyword,startDate,endDate,uid)
    
    #weiboParser.DBoperation()
    outPath = './'+outPath + '.xls'
    utils.writeXL(contentsDict,outPath)
    
if __name__ == '__main__' : 
    main()