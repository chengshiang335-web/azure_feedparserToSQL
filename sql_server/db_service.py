import datetime
import os
import json
import pymssql
import sys

# 將上一層目錄加入系統路徑，以讀取 configLoader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configLoader.config_loader import load_db_config



def insert_to_db(df):
    """
    寫回 SQL
    """
    #print(f"準備寫入 {len(records)} 筆資料...")
    # 透過 config_loader 載入環境變數或 local.settings.json 設定
    db_config = load_db_config()

    if not db_config:
        return "錯誤: 無法載入資料庫設定"

    server = db_config.get("db_server")
    database = db_config.get("database")
    table_name = db_config.get("table_name")
    user = db_config.get("user")
    password = db_config.get("password")
    
    print(f"資料庫設定載入成功: server={server}, database={database}, table={table_name}")


    if not all([server, database, user, password]):
        return "錯誤: 環境變數未設置"
    
    INS_SQL = """
        INSERT into dbo.News(uid, title, link, published) 
        VALUES (
            %s,
            %s,
            %s,
            %s
        )
    """
    try:
        connect = pymssql.connect(server, user, password, database)
        cursor = connect.cursor()
        print("資料庫連線成功")

        # 假設 md5Key 是 PK
        cursor.execute(f"SELECT uid FROM dbo.{table_name}")
        existing = {row[0] for row in cursor.fetchall()}
        print(f"過滤前共有 {len(df)} 筆資料，資料庫中已有 {len(existing)} 筆資料")
        df = df[~df['uid'].isin(existing)]
        print(f"過濾後剩 {len(df)} 筆新資料需要寫入資料庫...")
        #將 DataFrame 轉 list of tuples
        records = df[['uid', 'title', 'link', 'published']].values.tolist()
        records_tuples = [tuple(x) for x in records]
        #print(f"準備寫入 {len(records_tuples)} 筆資料到資料庫...")
        #寫入資料
        cursor.executemany(INS_SQL, records_tuples)
        connect.commit()

        print("資料寫入完畢")
    finally:
        cursor.close()
        connect.close()
