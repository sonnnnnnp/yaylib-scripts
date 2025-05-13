# 2025/5/11
# group_idsに入れたグループのユーザーの参加、脱退を検知してDiscordに通知する
# 
import time
import json
import requests
import yaylib

bot = yaylib.Client()
group_ids = [186466, 360253, 360254]
group_names = ['C/C++', 'JavaScript', 'Python']
webhook_url = 'https://discord.com/api/webhooks/xxxxxxx/yyyyyyyy'

def send_discord_notification(user_id, group_name, text):
    data = {
        'content': f'{group_name}{text}\nhttps://yay.space/user/{user_id}'
    }
    response = requests.post(webhook_url, json=data)
    if not response.status_code == 204:
        print(f'Failed to send notification: {response.status_code}')

while True:
    with open('group_users.json', 'r') as f:
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

            if len(users) < 20:  # 1回取得できる最大件数(20件)未満ならもうない
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
            send_discord_notification(user_id, group_names[i], 'に参加しました')
        for user_id in removed:
            send_discord_notification(user_id, group_names[i], 'を脱退しました')

    with open('group_users.json', 'w') as f:
        json.dump(new_data, f, indent=4)

    time.sleep(60 * 5)  # 5分待機
