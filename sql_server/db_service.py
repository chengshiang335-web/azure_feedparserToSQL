import datetime
import os
import json
import pymssql
import sys
import logging
import time


# 將上一層目錄加入系統路徑，以讀取 configLoader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configLoader.config_loader import load_db_config
from Line import lineMsg
# 設定 logging 基本配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


import os
import time
import logging
import pymssql


def get_conn(retry=5, delay=5, timeout=5):
    """
    建立 SQL Server 連線（含重試 + 喚醒檢查）
    """
    for attempt in range(1, retry + 1):
        try:
            logging.info(f"[DB] 嘗試連線 ({attempt}/{retry})")

            conn = pymssql.connect(
                server=os.getenv("DB_SERVER"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                login_timeout=timeout,
                timeout=timeout
            )

            # ✅ 驗證連線（避免假連線成功）
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            logging.info("[DB] 連線成功 ✅")
            return conn

        except pymssql.OperationalError as e:
            logging.error(f"[DB] 連線失敗 (attempt {attempt}): {e}")

        except Exception as e:
            logging.error(f"[DB] 未知錯誤: {e}", exc_info=True)

        # ⏳ 指數退避（避免狂打 DB）
        sleep_time = delay * attempt
        logging.info(f"[DB] 等待 {sleep_time} 秒後重試...")
        time.sleep(sleep_time)

    # ❌ 全部失敗
    raise Exception("[DB] 無法連線，已達最大重試次數")

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
    line_user_id = db_config.get("line_user_id")    
    print("a line_user_id: ", line_user_id)

    print(f"資料庫設定載入成功: server={server}, database={database}, table={table_name}")

    if not all([server, database, user, password]):
        print("錯誤: 環境變數未設置完整")
        return "錯誤: 環境變數未設置"

    connect = get_conn()
    
    cursor = None
    if connect:
        print("資料庫連線成功")

        try:
            cursor = connect.cursor()
            cursor.execute(f"SELECT uid FROM dbo.{table_name}")
            existing = {row[0] for row in cursor.fetchall()}

            print(f"過濾前共有 {len(df)} 筆資料，資料庫中已有 {len(existing)} 筆資料")
            df = df[~df['uid'].isin(existing)]
            print(f"過濾後剩 {len(df)} 筆新資料需要寫入資料庫...")

            # 將 DataFrame 轉 list of tuples
            records_tuples = [tuple(x) for x in df[['uid', 'title', 'link', 'published']].values]

            if records_tuples:
                INS_SQL = """
                    INSERT INTO dbo.News(uid, title, link, published) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.executemany(INS_SQL, records_tuples)
                connect.commit()
                print(f"資料寫入完畢，共寫入 {len(records_tuples)} 筆")

                titles = df['title'].tolist()
                msg = os.linesep.join(titles)  # 依作業系統換行
                print(msg)
                lineMsg.send_line(msg, line_user_id)

            else:
                print("沒有新資料需要寫入")

        except Exception as e:
            print(f"資料庫操作發生錯誤  {e}")

        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()
            print("資料庫連線已關閉")


    else:
        print("資料庫連線失敗")
        return "資料庫連線失敗"

    