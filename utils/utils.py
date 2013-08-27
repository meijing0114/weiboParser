#encoding= utf-8
import xlwt

def urlGenerate(weiboIDs):
    urls = []
    for weiboID in weiboIDs[:]:
        weiboID = weiboIDDict[shopID]
        url = 'http://weibo.cn/' % weiboID
        urls.append(url)
    return urls
     
def writeXL(contentsDict,outPath):
    
    demo = xlwt.Workbook()
    table1 = demo.add_sheet('sheet1',cell_overwrite_ok=True)
    # font info
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    # Initialize a style
    style = xlwt.XFStyle()
    style.font = font
        
    table1.write(0,0,'weiboID',style)
    table1.write(0,1,'Content',style)
    table1.write(0,2,'zan',style)
    table1.write(0,3,'zhuanfa',style)
    table1.write(0,4,'pinglun',style)
    row = 1
    keys = contentsDict.keys()
    for key in keys:
        print key
        infos = contentsDict[key]
        table1.write(row,0,key)
        if len(infos) ==0:
            print "empty list exist!"
        for info in infos:
            col = 0
            col = col + 1
            for msg in info:
                table1.write(row,col,str(msg).decode('utf-8'))
                col = col + 1
            row = row + 1
        
    demo.save(outPath)  

