import requests as requests   
import json

CHANNEL_ACCESS_TOKEN = "pwn6r1cIEvWZ1nBUJU49MewToxa6c3ibWnS08Mez87lVWsrCJPgGy9hvg05yUhhFz8D/pwWQ99GXI6dkPBEUxq7Ci0/zrbiyXld0cpayON9XaNA84GvvYiXnvyXN1CD7pwltw0zt3XGg/CrQNTadSQdB04t89/1O/w1cDnyilFU="
USER_ID = "U6d33aecb7e8b4bc3d7c6e9769fbf2cdc" #USER
#USER_ID = "U80ba6d03da8ea8769d2fd4b6fdd63696" #翔翔

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
    msg = "翔翔主人您好：我想問問看哥哥要不要去學校運動!!"
    #send_line(msg,USER_ID)
    broadcast_msg(msg)
    print("end test")