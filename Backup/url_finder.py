import requests
# pip install requests
from bs4 import BeautifulSoup
# Beautiful Soup(bs4) is a Python library for pulling data out of HTML and XML files. 

def URL_Finder (url):
    # url = 'https://news.ycombinator.com'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    urls = set() #unique
    str="http"
    for link in soup.find_all('a'):
        if link.get('href')!=None:
            url_temp=link.get('href')
            if str in url_temp:
                urls.add(url_temp)
            # print(urls)
    return urls

# Start from Here
urls=set() #unique
url_origin='https://news.ycombinator.com'
urls_first=URL_Finder(url_origin)
urls=URL_Finder(url_origin)
count=len(urls_first)
for links in urls_first:
    if len(urls)>=100:
        break
    urls_second=URL_Finder(links)
    urls.update(urls_second)
    count+=len(urls_second)

count = 0
for elem in iter(urls):
    if count == 100: #first 100
        break
    print(elem)
    count += 1

