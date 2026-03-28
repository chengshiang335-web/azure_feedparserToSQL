import datetime
import os
import json
import pymssql
import sys
import logging
import lineMsg as lineMsg

# 將上一層目錄加入系統路徑，以讀取 configLoader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configLoader.config_loader import load_db_config

# 設定 logging 基本配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def insert_to_db(df):
    """
    寫回 SQL Server
    """
    db_config = load_db_config()
    if not db_config:
        logging.error("錯誤: 無法載入資料庫設定")
        return "錯誤: 無法載入資料庫設定"

    server = db_config.get("db_server")
    database = db_config.get("database")
    table_name = db_config.get("table_name")
    user = db_config.get("user")
    password = db_config.get("password")

    logging.info(f"資料庫設定載入成功: server={server}, database={database}, table={table_name}")

    if not all([server, database, user, password]):
        logging.error("錯誤: 環境變數未設置完整")
        return "錯誤: 環境變數未設置"

    INS_SQL = """
        INSERT INTO dbo.News(uid, title, link, published) 
        VALUES (%s, %s, %s, %s)
    """

    connect = None
    cursor = None
    try:
        logging.info("開始連線資料庫")
        connect = pymssql.connect(server, user, password, database)
        cursor = connect.cursor()
        logging.info("資料庫連線成功")

        # 假設 uid 是 PK
        cursor.execute(f"SELECT uid FROM dbo.{table_name}")
        existing = {row[0] for row in cursor.fetchall()}

        logging.info(f"過濾前共有 {len(df)} 筆資料，資料庫中已有 {len(existing)} 筆資料")
        df = df[~df['uid'].isin(existing)]
        logging.info(f"過濾後剩 {len(df)} 筆新資料需要寫入資料庫...")

        # 將 DataFrame 轉 list of tuples
        records_tuples = [tuple(x) for x in df[['uid', 'title', 'link', 'published']].values]

        if records_tuples:
            cursor.executemany(INS_SQL, records_tuples)
            connect.commit()
            logging.info(f"資料寫入完畢，共寫入 {len(records_tuples)} 筆")
        else:
            logging.info("沒有新資料需要寫入")

    except Exception as e:
        logging.error("資料庫操作發生錯誤", exc_info=True)

    finally:
        if cursor:
            cursor.close()
        if connect:
            connect.close()
        logging.info("資料庫連線已關閉")

        for msg in df['title']:
            lineMsg.send_line(msg)