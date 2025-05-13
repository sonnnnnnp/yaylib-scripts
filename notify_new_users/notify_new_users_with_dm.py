# 2025/5/12
# Discord通知だけじゃなく、参加者にWelcomeメッセージを送信する(脱退者にも悲しみのメッセージを送信する)
#

# メッセージを送信するアカウントのメールアドレスとパスワードを指定
email = "user@example.com"
password = "password"

import time
import json
import requests
import yaylib

bot = yaylib.Client()

group_ids = [186466, 360253, 360254]
group_names = ["C/C++", "JavaScript", "Python"]
webhook_url = "https://discord.com/api/webhooks/xxxxxxx/yyyyyyyy"

def send_discord_text(text):
    data = {"content": text}
    response = requests.post(webhook_url, json=data)
    if not response.status_code == 204:
        print(f"Failed to send notification: {response.status_code}")

def send_discord_notification(user_id, group_name, text):
    send_discord_text(f"{group_name}{text}\nhttps://yay.space/user/{user_id}")

def nickmsg(user_id):
    try:
        nickname = bot.get_user(user_id).data["user"]["nickname"]
        return f"こんにちは{nickname}さん"
    except Exception as e:
        send_discord_text(f"Error fetching nickname for user {user_id}: {e}")
        return ""


def send_group_message(user_id, group_name, mode="welcome"):
    msg_bot = yaylib.Client()
    msg_bot.login(email=email, password=password)

    if mode == "welcome":
        message = f"{nickmsg(user_id)}\nようこそ、{group_name}サークルへ！\nあなたの参加を心より歓迎します。\n(これはYaylibを使用して自動送信されたメッセージです)"
    elif mode == "goodbye":
        message = f"{nickmsg(user_id)}さん\nえっ……ほんとに抜けちゃったの？\n{group_name}サークルは、あなたがいたあの空気、忘れません。\nちょっとでも「また話したいな」って思ったら、いつでも戻ってきてね。\nドアはずっと開けて待ってます。\n(これはYaylibを使用して自動送信されたメッセージです)"
    else:
        raise ValueError("mode must be either 'welcome' or 'goodbye'")

    chat_room_id = msg_bot.create_private_chat(
        with_user_id=user_id, hima_chat=True
    ).data["room_id"]
    msg_bot.send_message(chat_room_id=chat_room_id, text=message)
    # print(message)


while True:
    try:
        with open("group_users.json", "r") as f:
            old_data = json.load(f)
        new_data = {}
        for group_id in group_ids:
            all_users = []
            all_user_ids = []
            from_id = None

            while True:
                params = {}
                if from_id is not None:
                    params["from_id"] = from_id

                response = bot.get_group_members(group_id, **params)
                users = response.data["group_users"]

                if not users:
                    break

                all_users.extend(users)

                from_id = users[-1]["user"]["id"]  # 次のページの起点にする

                if len(users) < 20:  # 1ページの最大件数未満ならもうない
                    break

            for user in all_users:
                user_id = user["user"]["id"]
                all_user_ids.append(user_id)
            new_data[group_id] = all_user_ids

        for i, group_id in enumerate(group_ids):
            old_data_set = set(old_data[str(group_id)])
            new_data_set = set(new_data[group_id])
            removed = list(old_data_set - new_data_set)
            added = list(new_data_set - old_data_set)
            for user_id in added:
                send_group_message(user_id, group_names[i])
                send_discord_notification(user_id, group_names[i], "に参加しました")
            for user_id in removed:
                send_group_message(user_id, group_names[i], mode="goodbye")
                send_discord_notification(user_id, group_names[i], "を脱退しました")

    except Exception as e:
        send_discord_text(f"Error: {e}")
        print(f"Error: {e}")

    with open("group_users.json", "w") as f:
        json.dump(new_data, f, indent=4)

    time.sleep(60 * 5)  # 5分待機
