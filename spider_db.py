from bs4 import BeautifulSoup
import lxml
import re
import MySQLdb
class DATA():
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = ''
        self.passwd = ''
    
    def GetLinkDB(self):
        self.user = raw_input("user:")
        self.passwd = raw_input("pwd:")
        db = MySQLdb.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                passwd = self.passwd
                )
        return db

    def CreateDB(self,db):
        linkdb = db.cursor()
        linkdb.execute("create database wooyun_bug")
        linkdb.execute("use wooyun_bug")
        linkdb.execute("create table bug_info(bug_id varchar(20),bug_url varchar(50),bug_title varchar(200),bug_author varchar(20))")
        linkdb.close()
        print "create table OK!"

    def InsertData(self,db,bug_id,bug_url,bug_title,bug_author):
        linkdb = db.cursor()
        sqli = "insert into bug_info values(%s,%s,%s,%s)"
        linkdb.execute(sql,(bug_id,bug_url,bug_title,bug_author))
        print "execute OK!"
        linkdb.close()
        db.commit()
        print "Insert OK!"

    def SelectData(self,db):
        sqli = "select * from bug_info"
        linkdb = db.cursor()
        bugs = linkdb.execute(sqli)
        for i in linkdb.fetchmany(bugs):
            print i[0],i[1],i[2].decode("utf-8"),i[3].decode("utf-8")
        linkdb.close()
    
    def CloseDB(self,db):
        db.close()

DB = DATA()
db = DB.GetLinkDB()
DB.CreateDB(db)
f = open("WooYun.html","r")
soup = BeautifulSoup(f,"lxml")
for tr in soup.tbody.find_all('tr'):
    bug_title = tr.find("td").a.string.encode("utf-8")
    bug_url = tr.find("td").a.get("href").encode("utf-8")
    bug_author = tr.find_all_next("th")[2].a.get("title").encode("utf-8")
    bug_id = re.sub("http://www.wooyun.org/bugs/","",bug_url).encode("utf-8")
    DB.InsertData(db,bug_id,bug_url,bug_title,bug_author)
DB.SelectData(db)
DB.CloseDB(db)
