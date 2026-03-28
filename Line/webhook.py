from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.json
    print("Received:", data)
    # 回傳 200 給 LINE
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)