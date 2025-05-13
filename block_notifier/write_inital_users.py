# 2025/5/14
# ブロックしているユーザーをcsvに書き込む
# (初回実行時に大量の通知が来ないようにするため)
# (blocker_ids.csvが存在しない場合自動でファイル作成されます)

import csv
import yaylib

email = "your@email.com"
password = "your_password"

bot = yaylib.Client()
bot.login(email, password)

ids = bot.get_blocked_user_ids().data["block_ids"]

with open("blocker_ids.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(ids)