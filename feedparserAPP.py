#套件來源
#https://github.com/kurtmckee/feedparser

import sys
import os
# 將上一層目錄加入系統路徑，這樣 Python 就能找到外部的 configLoader 資料夾
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import feedparser
import pandas as pd
import hashlib
import sql_server.db_service as db_service
import datetime


def main():

    #rss_url = "https://rss.app/feeds/4puCMmnqU1SmJB9v.xml"
    rss_url = "https://news.google.com/rss/search?q=Donald+Trump&site:cnn.com&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"


    feed = feedparser.parse(rss_url)
    data = []
    #print(f"len:{len(feed.entries)}")

    for entry in feed.entries:
        
        pub_struct = entry.published_parsed if 'published_parsed' in entry else None
    
        sql_published = datetime.datetime.strftime(datetime.datetime(*pub_struct[:6]), '%Y-%m-%d %H:%M:%S')
        
        data.append({
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": sql_published,
            "md5Key": hashlib.md5(entry.get("link", "").encode()).hexdigest()
        })

    df = pd.DataFrame(data)
    print(f"總共處理了 {len(df)} 筆資料")
    #print(df['published'])
    # 將整理好的 df 以及設定檔的參數，傳遞給專門處理寫入 SQL Server 的元件
    db_service.insert_to_db(df)
