from bs4 import BeautifulSoup
import urllib
from urllib import request
import re
import time
import sys
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

global already_checked
global start_time

start_time = time.time()

already_checked = []

def check_for_pirate_bay(url):
    global already_checked
    if url in already_checked: return False
    if url[0] == '/': return False
    already_checked.append(url)
    if len(already_checked) % 10 == 0: print("Checked", len(already_checked), "sites.")
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        html_page = urllib.request.urlopen(req, timeout=5)
    except:
        return False
    mybytes = html_page.read()
    try:
        body = mybytes.decode("utf8")
    except:
        body = ''
    html_page.close()
    if "Pirate Search" in body:
        return True
    return False

def get_urls(url):
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    try:
        html_page = urllib.request.urlopen(req)
    except:
        return None
    soup = BeautifulSoup(html_page, features='lxml')
    out_urls = []
    for link in soup.findAll('a'):
        current_url = link.get('href')
        if current_url is None: continue
       # if current_url[0] == '/': continue
        if 'google.com' in current_url: continue
        slash_count = current_url.count('/')
        if slash_count != 3 or current_url[-1] != '/': continue
        out_urls.append(current_url)
    return out_urls

print("Finding Pirate Bay proxy sites")
visited_urls = []
query = 'pirate bay proxy'
k = 0
for i in range(0,1000):
    print("page ", i)
    for j in search(query, num=10, start=i*10, stop=i*10+10, pause=7.0):
        k += 1
        url = j
        if url in visited_urls: continue
        out_url = url
        urls = get_urls(out_url)
        if urls is None: urls = []
        for url in urls:
            is_pirate_bay = check_for_pirate_bay(url)
            if is_pirate_bay:
                time_spent = time.time() - start_time
                print("Pirate bay proxy:", url, "(found in", str(int(time_spent)), "seconds)")
        visited_urls.append(url)