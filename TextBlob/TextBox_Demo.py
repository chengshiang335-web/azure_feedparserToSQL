from textblob import TextBlob  # 導入 TextBlob 函式庫
import feedparser
import datetime
import hashlib
from zoneinfo import ZoneInfo
import os

# rss_url = "https://news.google.com/rss/search?q=Donald+Trump&site:cnn.com&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
# feed = feedparser.parse(rss_url)
rss_url = "https://news.google.com/rss/search?q=Donald+Trump&site:cnn.com&hl=en-US&gl=US&ceid=US:en"
feed = feedparser.parse(rss_url)


data = []
countFreed = 0

for entry in feed.entries:
    countFreed += 1
    pub_struct = entry.published_parsed if 'published_parsed' in entry else None

    if pub_struct:
        dt_utc = datetime.datetime(*pub_struct[:6], tzinfo=ZoneInfo("UTC"))
        dt_tw = dt_utc.astimezone(ZoneInfo("Asia/Taipei"))
        sql_published = dt_tw.strftime('%Y-%m-%d %H:%M:%S')
        
        # --- 串接 TextBlob 情感分析 ---
        title = entry.get("title", "")
        blob = TextBlob(title)
        # sentiment 屬性會回傳 polarity (極性) 與 subjectivity (主觀性)
        sentiment_score = blob.sentiment 
        
        data.append({
            "title": title,
            "link": entry.get("link"),
            "published": sql_published,
            "uid": hashlib.md5(entry.get("link", "").encode()).hexdigest(),
            "polarity": sentiment_score.polarity,      # 範圍：-1.0 (負面) 到 1.0 (正面)
            "subjectivity": sentiment_score.subjectivity # 範圍：0.0 (客觀) 到 1.0 (主觀)
        })

        print(f"title: {title}")
        print(f"polarity: {sentiment_score.polarity} subjectivity:{sentiment_score.subjectivity}")
        print   ("-------------------")

    else:
        print(f"第 {countFreed} 筆資料缺少 published_parsed 欄位，已跳過。")

    
    # for item in data:
    #     print(item["title"])
    #print(data) 
    #print(f"countFreed: {countFreed}    ")
    #print(f"polarity: {sentiment_score.polarity}, subjectivity: {sentiment_score.subjectivity}  ")
 
# for item in data:
#     print(item)
