from bs4 import BeautifulSoup
import lxml
import re
import MySQLdb
class Data:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = ''
        self.passwd = ''
    
    def GetLinkDB(self):
        self.user = 'root'
        self.passwd = '123456'
        link = MySQLdb.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                passwd = self.passwd
                )
        return link

    def CreateDB(self,link):
        try:
            linkdb = link.cursor()
            linkdb.execute("create database wooyun_bug_test")    #create database
        except MySQLdb.Error,e:                             #if database exist pass
            if e[0] == 1007:
                print "database exist!"
                pass
        else:
            print "create database OK!"
        linkdb.execute("use wooyun_bug_test")
        try:
            linkdb.execute("create table bug_info(bug_id varchar(50),bug_url varchar(100),bug_title varchar(400),bug_author varchar(150))")
        except MySQLdb.Error,e:                             #if table exist pass
            if e[0] == 1050:
                print "table exist!"
                pass
        else:
            print "create table OK!"
        linkdb.close()

    def InsertData(self,link,bug_id,bug_url,bug_title,bug_author):
        linkdb = link.cursor()
        sqli = "insert into bug_info values(%s,%s,%s,%s)"
        linkdb.execute(sqli,(bug_id,bug_url,bug_title,bug_author))
        linkdb.close()
        link.commit()

    def SelectData(self,link):
        sqli = "select bug_id from bug_info"
        linkdb = link.cursor()
        bugs = linkdb.execute(sqli)
        for i in linkdb.fetchmany(bugs):
            print i[0]
        linkdb.close()
    
    def CloseDB(self,link):
        link.close()
if __name__ == "__main__":
    try:
        DB = Data()
        db = DB.GetLinkDB()
        DB.CreateDB(db)
    except MySQLdb.Error,e:
        print "Error Code:%d\nError Reason:%s"%(e[0],e[1])
    else:
        f = open("WooYun.html","r")
        soup = BeautifulSoup(f,"lxml")
        for tr in soup.tbody.find_all('tr'):
            bug_title = tr.find("td").a.string.encode("utf-8")
            bug_url = tr.find("td").a.get("href").encode("utf-8")
            bug_author = tr.find_all_next("th")[2].a.get("title").encode("utf-8")
            bug_id = re.sub("http://www.wooyun.org/bugs/","",bug_url).encode("utf-8")
            try:
                DB.InsertData(db,bug_id,bug_url,bug_title,bug_author)
            except MySQLdb.Error,e:
                print "Error Code:%d\nError Reason:%s"%(e[0],e[1])
        DB.SelectData(db)
        DB.CloseDB(db)
