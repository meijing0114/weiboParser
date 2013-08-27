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
    
    # Read in the weiboID dict with shopIDs from db
    weiboIDs = raw_input('Input weiboID(number or string) that you want to parse, split by "," : ')
    username = raw_input('Please input username: ')
    pwd = raw_input('Please input weibo Password: ')
    weiboIDs = weiboIDs.split(',') 
    day = int(raw_input('How many days of weibo do you neeed? '))
    validDay = currentYear*12*30 + currentMonth*30 + currentDay - day
    outPath = raw_input('Input file name to save the results:')   
    proxy_ip = raw_input('Please input the proxy ip:')
    proxy_port = raw_input('Please input the proxy port:')
    proxy = proxy_ip + ':' + proxy_port
    # Create an weiboCNParser instance and start parsing
    print "Start parsing...\n"
    weiboParser = weiboCNParser.weiboCNParser(username, pwd,validDay,proxy)
    contentsDict = weiboParser.weiboCNContentParser(weiboIDs)
    #weiboParser.DBoperation()
    outPath = './'+outPath + '.xls'
    utils.writeXL(contentsDict,outPath)
    
if __name__ == '__main__' : 
    main()