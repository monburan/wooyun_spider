import requests
from bs4 import BeautifulSoup
import lxml
import re
import MySQLdb
import time

class Data:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = ''
        self.passwd = ''
    
    def GetLinkDB(self):
        self.user = raw_input("user:")
        self.passwd = raw_input("pwd:")
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
            linkdb.execute("create database wooyun_bug")
        except MySQLdb.Error,e:
            if e[0] == 1007:
                pass
        else:
            print "create database OK!"
        linkdb.execute("use wooyun_bug")
        try:
            linkdb.execute("create table bug_info(bug_id varchar(50),bug_url varchar(100),bug_title varchar(400),bug_author varchar(150))")
        except MySQLdb.Error,e:
            if e[0] == 1050:
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
        sqli = "select count(bug_id) from bug_info"
        linkdb = link.cursor()
        bugs = linkdb.execute(sqli)
        for i in linkdb.fetchmany(bugs):
            print i
#            print i[0],i[1],i[2].decode("utf-8"),i[3].decode("utf-8")
        linkdb.close()
    
    def CloseDB(self,link):
        link.close()
class Wooyun:
    def __init__(self):
        self.url = 'http://wooyun.org/bugs/new_public/'
        self.headers = {
            "Host":"wooyun.org",
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding":"gzip, deflate",
            "Referer":"http://wooyun.org/",
            "Connection":"keep-alive"
        }
        self.page = 1
        self.data = Data()

    def GetPageNum(self):
        response = requests.get(self.url,headers = self.headers)
        soup = BeautifulSoup(response.text,"lxml")
        pagenum = re.compile("(\d+)").findall(soup.p.strings.next())
        return int(pagenum[1])

    def MakeHeaders(self,page):
        headers = self.headers
        if page == 1:
            url = self.url
            return url,headers
        if page == 2:
            url = self.url + "page/" + str(page)
            headers["Referer"] = "http://wooyun.org/bugs/new_public"
            return url,headers
        if page > 2:
            url = self.url + "page/" +str(page)
            headers["Referer"] = "http://wooyun.org/bugs/new_public/page/" + str(page-1)
            return url,headers
    def GetBugList(self,link,url,headers):
        html = requests.get(url,headers = headers)
        soup = BeautifulSoup(html.text,"lxml")
        for tr in soup.tbody.find_all('tr'):
            try:
                bug_title = tr.find("td").a.string.encode("UTF-8")
                bug_url = 'http://wooyun.org' + tr.find("td").a.get("href").encode("UTF-8")
                bug_author = tr.find_all_next("th")[2].a.get("title").encode("UTF-8")
                bug_id = re.sub("/bugs/","",tr.find("td").a.get("href")).encode("UTF-8")
            except AttributeError,e:
                print "have an error : %s"%(e)
            else:
                self.data.InsertData(link,bug_id,bug_url,bug_title,bug_author)

    def main(self):
        try:
            link = self.data.GetLinkDB()
            self.data.CreateDB(link)
        except MySQLdb.Error,e:
            print"Error Code:%d\nError Reason:%s"%(e[0],e[1])
        
        max_page = self.GetPageNum()
        for i in range(1,max_page):
            mk = self.MakeHeaders(i)
            self.GetBugList(link,mk[0],mk[1])
            print "Get Page %d All Bug..."%(i)
            time.sleep(2)
        self.data.SelectData(link)
        self.data.CloseDB(link)
        
if __name__ == "__main__":
    wy = Wooyun()
    wy.main()
