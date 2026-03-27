import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
from zoneinfo import ZoneInfo
import datetime
import hashlib
import logging
import pandas as pd
import feedparser

# 將上一層目錄加入系統路徑
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sql_server.db_service as db_service

# 設定 logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    logging.info("version: 2024-06-17 22:00 by python")   
    print("version: 2024-06-17 15:00")

    rss_url = "https://news.google.com/rss/search?q=Donald+Trump&site:cnn.com&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    feed = feedparser.parse(rss_url)

    data = []
    countFreed = 0

    for entry in feed.entries:
        countFreed += 1
        pub_struct = entry.published_parsed if 'published_parsed' in entry else None

        if pub_struct:
            # UTC 時間
            dt_utc = datetime.datetime(*pub_struct[:6], tzinfo=ZoneInfo("UTC"))
            # 轉台灣時間
            dt_tw = dt_utc.astimezone(ZoneInfo("Asia/Taipei"))

            sql_published = dt_tw.strftime('%Y-%m-%d %H:%M:%S')
            data.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": sql_published,
                "uid": hashlib.md5(entry.get("link", "").encode()).hexdigest()
            })
        else:
            logging.warning(f"第 {countFreed} 筆資料缺少 published_parsed 欄位，已跳過。")

    logging.info(f"countFreed: {countFreed}")
    logging.info(f"len(feed.entries): {len(feed.entries)}")
    logging.info(f"總共處理了 {len(data)} 筆資料")

    df = pd.DataFrame(data)

    # 寫入資料庫
    db_service.insert_to_db(df)


if __name__ == "__main__":
    main()