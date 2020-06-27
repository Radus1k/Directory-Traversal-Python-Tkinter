#!/usr/bin/python
import urllib.error
import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup
import time

def getAllUrl(url, start_time):
    curr_time = time.time()
    while curr_time - start_time < 30:
        try:
            page = urllib.request.urlopen(url).read()
        except:
            return []
        urlList = []
        try:
            soup = BeautifulSoup(page, features="html.parser")
            soup.prettify()
            for anchor in soup.findAll('a', href=True):
                if not 'http://' in anchor['href']:
                    if urllib.parse.urljoin(url, anchor['href']) not in urlList:
                        urlList.append(urllib.parse.urljoin(url, anchor['href']))
                else:
                    if anchor['href'] not in urlList:
                        urlList.append(anchor['href'])
                curr_time = time.time()
            length = len(urlList)

            return urlList
        except urllib.error.HTTPError as e:
            print("error:" + str(e))
        break

def listAllUrl(urlss):
    cur_time = time.time()
    for x in urlss:
        print(x)
        write_link_to_file(x)
        urlss.remove(x)
        urls_tmp = getAllUrl(x, cur_time)
        for y in urls_tmp:
            urlss.append(y)


def get_all_hyperlinks(page_content):
    hyperlinks_list = []
    soup = BeautifulSoup(page_content, features="html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("/*")}):
        # print(link.get('href')+"\n")
        hyperlinks_list = [hyperlinks_list, link.get('href')]
    #looking for Directory Traversal
    for link in soup.findAll('a', attrs={'href': re.compile("page=")}):
        # print(link.get('href') + "page founded: \n")
        hyperlinks_list = [hyperlinks_list, link.get('href')]
    return hyperlinks_list


def write_link_to_file(url_str):
    with open("links_of_current_web", "a") as f:
        f.write(url_str + "\n")
    f.close()


def generate_web_urls(url_string):
    urls = [url_string]
    while len(urls) > 0:
        urls = getAllUrl(url_string)
        listAllUrl(urls)

