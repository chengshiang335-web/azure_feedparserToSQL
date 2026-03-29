import requests as requests   
import json
import os


CHANNEL_ACCESS_TOKEN =   os.getenv("CHANNEL_ACCESS_TOKEN"),

def send_line(msg,user_id):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }

    data = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": msg
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # 印出狀態碼與回傳內容
        print(f"HTTP Status: {response.status_code}")
        print(f"Response Body: {response.text}")

        # 如果不是 200，代表推播失敗
        if response.status_code != 200:
            print("推播失敗！")
            return False
        return True
    except Exception as e:
        print(f"例外錯誤: {e}")
        return False


def broadcast_msg(msg):
    url = "https://api.line.me/v2/bot/message/broadcast"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }

    data = {
        "messages": [
            {
                "type": "text",
                "text": msg
            }
        ]
    }

    try :
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # 印出狀態碼與回傳內容
        print(f"HTTP Status: {response.status_code}")
        print(f"Response Body: {response.text}")

        # 如果不是 200，代表推播失敗
        if response.status_code != 200:
            print("推播失敗！")
            return False
        return True
    except Exception as e:
        print(f"例外錯誤: {e}")
        return False



if __name__ == "__main__":
    print("start test")
    msg = "翔翔主人您好：這是Line開發者測試信!!"

    LINE_USER_ID =  os.getenv("LINE_USER_ID")
    send_line(msg,LINE_USER_ID)
    #broadcast_msg(msg)
    print("end test")