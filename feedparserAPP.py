#套件來源
#https://github.com/kurtmckee/feedparser

import sys
import os
from zoneinfo import ZoneInfo
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

    rss_url = "https://news.google.com/rss/search?q=Donald+Trump&site:cnn.com&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    countFreed=0

    for entry in feed.entries:
        countFreed += 1
        pub_struct = entry.published_parsed if 'published_parsed' in entry else None
        #print("published_parsed:", pub_struct)
        if pub_struct:
            # UTC 時間
            dt_utc = datetime.datetime(*pub_struct[:6], tzinfo=ZoneInfo("UTC"))
            # 轉台灣時間
            dt_tw = dt_utc.astimezone(ZoneInfo("Asia/Taipei"))
            #print(f"原始: {entry.published} | UTC: {dt_utc} | 台灣: {dt_tw}")

            sql_published = dt_tw.strftime('%Y-%m-%d %H:%M:%S')
            data.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": sql_published,
                "uid": hashlib.md5(entry.get("link", "").encode()).hexdigest()
    })

    else:
        print(f"第 {countFreed} 筆資料缺少 published_parsed 欄位，已跳過。")

    print(f"countFreed: {countFreed}    ")   

    print(f"len:{len(feed.entries)}")

    #print(f"原始: {entry.published} | UTC: {dt_utc} | 台灣: {dt_tw}")
    # 轉台灣時間
    


    df = pd.DataFrame(data)
    print(f"總共處理了 {len(df)} 筆資料")
    #print(df['published'])
    # 將整理好的 df 以及設定檔的參數，傳遞給專門處理寫入 SQL Server 的元件
    db_service.insert_to_db(df)


  
if __name__ == "__main__":
    main()