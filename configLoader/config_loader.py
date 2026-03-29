import os
import json

def load_db_config(config_path: str = None) -> dict:
    """
    通用版本：優先從環境變數讀取資料庫設定 (相容 Azure Functions & 本地端 local.settings.json)
    若環境變數中缺乏必要設定，則回傳 None。
    """
    # 嘗試載入本地端的 local.settings.json (如果尚未載入)
    if not os.getenv("DB_SERVER"):
        try:
            # 推算專案根目錄
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            settings_path = os.path.join(base_dir, "local.settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, encoding='utf-8') as f:
                    data = json.load(f)
                    for k, v in data.get("Values", {}).items():
                        if k not in os.environ:
                            os.environ[k] = str(v)
        except Exception:
            pass # 在 Azure 環境上或檔案不存在時忽略

    server = os.environ.get('DB_SERVER')
    user = os.environ.get('DB_USER', 'sa')
    password = os.environ.get('DB_PASSWORD', '')
    database = os.environ.get('DB_NAME', 'testdb')
    table_name = os.environ.get('TABLE_NAME', 'News')
    line_user_id = os.environ.get('LINE_USER_ID')

    if not server:
        print("環境變數中缺少資料庫必要設定 (DB_SERVER)")
        return None

    return {
        'db_server': server,
        'user': user,
        'password': password,
        'database': database,
        'table_name': table_name,
        'line_user_id': line_user_id    
    }
 