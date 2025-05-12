import yaylib, time
api = yaylib.Client()

import requests
from json import dumps
from datetime import datetime
headers = {'Content-Type': 'application/json'}
webhook_url = 'https://discord.com/api/webhooks/xxxxxxxx/yyyyyyy'
def send_discord(content):
    main_content = {
        'username': f'online_log.py',
        # 'avatar_url': ,
        'content': content,
    }
    requests.post(webhook_url, dumps(main_content), headers=headers)

users = {
    'カヲル': {'id': '4930835', 'status':  'offline'},
    '毛の可能性': {'id': '35152', 'status':  'offline'},
    '駆け出しアルパカ': {'id': '93', 'status':  'offline'},
}

def check_status():
    while True:
        for key in users:
            try:
                status = api.get_user(users[key]['id']).online_status
            except Exception as e:
                current_time = datetime.now()
                print(f"{current_time} エラーにょん: {e}")
            if status != users[key]['status']:
                send_discord(f'{key}が{status}になりました')
                # check_room(users[key]['id'],status)
            users[key]['status'] = status
        time.sleep(60)

check_status()

