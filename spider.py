import requests
from bs4 import BeautifulSoup
import lxml
import re

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

    def GetBugList(self,url,headers):
        html = requests.get(url,headers = headers)
        soup = BeautifulSoup(html.text,"lxml")
        for tr in soup.tbody.find_all('tr'):
            bug_title = tr.find("td").a.string
            bug_url = 'http://wooyun.org' + tr.find("td").a.get("href")
            bug_author = tr.find_all_next("th")[2].a.get("title")
            print bug_title,bug_url,bug_author
    
    def main(self):
        max_page = self.GetPageNum()
        for i in range(1,max_page):
            mk = self.MakeHeaders(i)
            self.GetBugList(mk[0],mk[1])
if __name__ == "__main__":
    wy = Wooyun()
    wy.main()
#    wy.GetBugList()
