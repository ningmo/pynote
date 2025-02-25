#coding:utf-8

import os
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlencode,quote_plus


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "host": "www.gequhai.com",
    "referer": "https://www.gequhai.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}
def search(name,song=''):
    filename = name + ".mp3"
    if os.path.exists(filename):
        print(filename,'exists')
        return
    print(name,song,'start')
    url = "https://www.gequhai.com/s/"+quote_plus(name)
    headers['referer'] = "https://www.gequhai.com/"
    res = requests.get(url,headers=headers)
    if res.status_code!=200:
        print(name,'搜索错误',res.text)
        return
    soup = BeautifulSoup(res.text,'html.parser')
    search_rows = soup.find_all('a','text-info', href=True)
    if len(search_rows)<1:
        print(name,'search not found')
        return
    for td in search_rows[0:3]:
        if td.string.strip() == name or name in td.string.strip():
            search_song = None
            if song in td.parent.next_sibling.string:
                search_song = td.parent.next_sibling.string.strip()
            elif song in td.parent.next_sibling.next_sibling.string:
                search_song = td.parent.next_sibling.next_sibling.string.strip()
            if not search_song:
                print(name,'songer not found')
                continue
            url_detail = 'https://www.gequhai.com'+td['href']
            headers['referer'] = url
            resDetail = requests.get(url_detail,headers=headers)
            if resDetail.status_code!=200:
                print(name,'详情错误',resDetail.text)
                continue
            matches = re.search("(window.play_id.*);",resDetail.text)
            if matches:
                play_id = matches.group().split('=')[1].replace("'",'').replace(";",'').strip()
                try:
                    resXhr = requests.post('https://www.gequhai.com/api/music', headers=headers, data={"id": play_id})
                    if resXhr.status_code != 200:
                        print('XHR错误', resXhr.text)
                        continue
                    res = json.loads(resXhr.text)
                    response = requests.get(res['data']['url'], headers={"Accept":'*/*',"referer":url}, stream=True)
                    if response.status_code != 200:
                        print(name,'下载错误', response.text)
                        continue
                    filename = name + ".mp3"
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    return
                except Exception as e:
                    print(name,'请求详情下载错误',e)

def main():
    for row in ss.split('\n'):
        if len(row)> 5 :
            s = [i for i in row.split(' ') if len(i)>=1]
            search(s[1].strip(),s[0].strip())
            print()

def scan():
    rows = []
    for s in  os.listdir('D:/music'):
        if not s.startswith('.'):
            rows.append(s.replace('.mflac','').replace('.flac','').replace('.mgg','').replace('-','   '))
    return rows

def compare():
    rows = scan()
    for row in rows:
        name_song = [x.strip() for x in row.split(' ') if len(x.strip())>=1]
        if not os.path.exists(name_song[1] + ".mp3"):
            print(name_song,'not exists')
