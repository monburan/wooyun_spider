import requests
from bs4 import BeautifulSoup
import lxml

url = 'http://wooyun.org/bugs/new_public/'
headers = {
        "Host":"wooyun.org",
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding":"gzip, deflate",
        "Referer":"http://wooyun.org/index.php",
        "Connection":"keep-alive"
        }
html = requests.get(url,headers=headers) 
soup = BeautifulSoup(html.text,"lxml")
for tr in soup.tbody.find_all('tr'):
    bug_title = tr.find("td").a.string
    bug_url = 'http://wooyun.org' + tr.find("td").a.get("href")
    bug_author = tr.find_all_next("th")[2].a.get("title")
    print bug_title,bug_url,bug_author
