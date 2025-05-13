# 2025/5/14
# ブロックしてきたユーザーをDiscordに通知

import time
import csv
import requests
import yaylib

email = "your@email.com"
password = "your_password"
webhook_url = "https://discord.com/api/webhooks/xxxxxxx/yyyyyyyy"

bot = yaylib.Client()
bot.login(email, password)

# discord通知関数
def send_discord(text):
    data = {"content": text}
    response = requests.post(webhook_url, json=data)
    if not response.status_code == 204:
        print(f"Failed to send notification: {response.status_code}")


while True:
    # csvからブロックしているユーザーのIDを取得
    with open("blocker_ids.csv", "r") as f:
        line = f.read()
        old_blocker_ids = line.strip().split(",")

    # yaylibからブロックしているユーザーのIDを取得
    new_blocker_ids = bot.get_blocked_user_ids().data["block_ids"]

    # 差分をDiscordに通知
    old_set = set(old_blocker_ids)
    new_set = set(map(str, new_blocker_ids))
    added = list(new_set - old_set)
    removed = list(old_set - new_set)
    for user_id in added:
        send_discord(f"https://yay.space/user/{user_id}\nがブロックしました\nあなたをブロックしているユーザー数: {len(new_blocker_ids)}")
    for user_id in removed:
        send_discord(f"https://yay.space/user/{user_id}\nがブロック解除かアカウントを削除しました\nあなたをブロックしているユーザー数: {len(new_blocker_ids)}")

    # csvを更新
    with open("blocker_ids.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(new_blocker_ids)

    time.sleep(60 * 5)  # 5分ごとにチェック
