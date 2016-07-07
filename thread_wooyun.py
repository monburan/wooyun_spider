import requests
from bs4 import BeautifulSoup
import lxml
import re
from time import sleep,ctime
import threading

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
        self.headers["Referer"] = "http://wooyun.org/bugs/new_public"
        self.page = 1

    def GetPageNum(self):
        response = requests.get(self.url,headers = self.headers)
        soup = BeautifulSoup(response.text,"lxml")
        pagenum = re.compile("(\d+)").findall(soup.p.strings.next())
        return int(pagenum[1])

    def bug_info(self,tr):
        try:
            bug_title = tr.find("td").a.string.encode("UTF-8")
            bug_url = 'http://wooyun.org' + tr.find("td").a.get("href").encode("UTF-8")
            bug_author = tr.find_all_next("th")[2].a.get("title").encode("UTF-8")
            bug_id = re.sub("/bugs/","",tr.find("td").a.get("href")).encode("UTF-8")
        except AttributeError,e:
            print "have an error : %s"%(e)
        else:
            return bug_id,bug_title,bug_url,bug_author

    def GetBugList(self,url,headers):
        print "get page bug"
        sleep(2)
        html = requests.get(url,headers)
        soup = BeautifulSoup(html.text,"lxml")
        result = []
        try:
            for tr in soup.tbody.find_all('tr'):
                result.append(self.bug_info(tr))
        except AttributeError,e:
            print html.text
        print "get end"

    def main(self):
        print 'starting at:',ctime()
        threads = []
        pagelist = range(0,10)
        for page in pagelist:
            url = self.url + "page/" +str(page)
            self.headers["Referer"] = "http://wooyun.org/bugs/new_public/page/" + str(page-1)
            headers = self.headers
            print headers
            t = threading.Thread(target = self.GetBugList,args=(url,headers))
            threads.append(t)

        for i in pagelist:
            print i
            threads[i].start()

        for i in pagelist:
            print i
            threads[i].join()
        print 'end at:',ctime()
if __name__ == "__main__":
    wy = Wooyun()
    wy.main()
