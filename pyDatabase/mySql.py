#encoding= utf-8
import MySQLdb

class sqlDB(object):
    def __init__(self):
        try:
            self.conn = MySQLdb.Connect(host='localhost',user='root',passwd = 'root',port=3306,charset='utf8')
            self.conn.select_db('attractions')
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" %(e.args[0],e.args[1])
            
    def readWeiboID(self,weiboIDDict):
        cur = self.conn.cursor()
        try:
            count = cur.execute('select weiboID,shopID from weiboid')
        except Exception:
            print "selecting weiboID failure"
        results = cur.fetchall()
        for result in results:
            key = result[1]
            weiboIDDict[key] = str(int(result[0]))
            
        cur.close()
        return weiboIDDict
    
    def readSearchStr(self, googleStrDict):
        cur = self.conn.cursor()
        try:
            count = cur.execute('select shopID,shopName from shopidsimple')
        except Exception:
            print "selecting shopidsimple failure"
        results = cur.fetchall()
        for result in results:
            key = result[0]
            googleStrDict[key] = result[1]
        cur.close()
        return googleStrDict
    def readFromDB(self):
        shopDict = {}
        cur = self.conn.cursor()
        cur.close()
    
    def writeToDB(self,shopDict,source):
        cur = self.conn.cursor()
        
        sql = "insert into results (shopID, theme, link, expireDate, source, isValid,content) values (%s,%s,%s,%s,%s,%s,%s)"
        keys = shopDict.keys()
        values = []
        for key in keys[:]:
            infos = shopDict[key]
            if len(infos):
                value = []
                for info in infos:
                # key as shopid, title, link, expireDate(08-12)
                    value = (key,info[0], info[1], info[2],source,0,info[3])
                    if self.notExist(value):
                        try:
                            cur.execute(sql,value)
                        except Exception:
                            print "insert into database results falilure!"
                    else:
                        print "Already Exist!"
                        continue;
            else:
                print "No activity for:" + str(key)
                continue;
        # 对于要插入的每一条记录，都去查询数据库中有没有相同的记录
        # 查询的方法是通过link 和 expireDate shopID
        self.conn.commit()
        cur.close()        
    
    def writeDataToDB(self, shopDict, source):
        cur = self.conn.cursor()
        sql = "insert into validationdata (content,isValid,source) values (%s,%s,%s)"
        keys = shopDict.keys()
        values = []
        for key in keys[:]:
            infos = shopDict[key]
            if len(infos):
                value = []
                for info in infos:
                # key as shopid, title, link, expireDate(08-12)
                    value = (info[3],0,source)
                    try:
                        cur.execute(sql,value)
                    except Exception:
                        print "insert into database results falilure!"
            else:
                print "No activity for:" + str(key)
                continue;
        # 对于要插入的每一条记录，都去查询数据库中有没有相同的记录
        # 查询的方法是通过link 和 expireDate shopID
        self.conn.commit()
        cur.close() 
    
    def notExist(self, value):
        cur = self.conn.cursor()
        print "value:"
        print value
        querySql = 'select * from results where shopID like %s and expireDate like %s and source like %s' %(value[0],value[3],value[4])
        count = 0
        try:
            count = cur.execute(querySql)
        except Exception:
            print "selecting error, existence."
        
        cur.close()
        
        if count == 0:
            return True
        elif count == 1:
            return False
        else :
            print "Error happens! Multiple exist"
            return False
            
        
    def __del__(self):
        self.conn.close()
        