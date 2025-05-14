# 2024/2/14
# Yaylibを使ったDM傍受 Discord転送bot
# 監視対象を自動で追加します


# 必要な3つのcsvファイル
# =========1=========
# settings.csv (設定用のwebhook)
#   1行目にlog出力用のwebhook
#   2行目に監視対象外のDMを転送webhook
# =========2=========
# target_list.csv (1行につき１人、監視したい対象のIDと転送先のwebhookを記載)
#   35152,https://discord.com/api/webhooks/...
#   4930835,https://discord.com/api/webhooks/...
# =========3=========
# opponents_ids.csv（監視対象に届いたDMの送信相手を自動で追加される、最低でも１つはIDを入れとかないとエラーになるから注意w）
# 93,808330622,129276...
# ===================




#
# JWT token
#
import time, hmac, hashlib
from json import dumps
from base64 import urlsafe_b64encode
class WSTokenGenerator:
    @staticmethod
    def get_token(user_id):
        timestamp = int(time.time())
        encode_payload = urlsafe_b64encode(f'{{"user_id":{user_id},"iat":{timestamp},"exp":{timestamp+30}}}'.encode()).decode().rstrip("=")
        payload = f"eyJhbGciOiJIUzI1NiJ9.{encode_payload}"
        sig = urlsafe_b64encode(hmac.new(key="6fa97fc2c3d04955bb8320f2d080593a".encode(),msg=payload.encode(),digestmod=hashlib.sha256,).digest()).decode().rstrip("=")
        return f'{payload}.{sig}'


#
# csv append
#
def csv_append(id):
    with open('opponents_ids.csv', 'a') as f:
        f.write(f',{id}')


#
# CSV => LIST
#
import csv
target_list = []
opponents_ids = []
target_dict = {}
with open('settings.csv') as f:
    for i, row in enumerate(csv.reader(f)):
        if i == 0:
            log_webhook = row[0]
        elif i == 1:
            others_webhook = row[0]

with open('target_list.csv') as f:
    for row in csv.reader(f):
        target_list.append(row)
target_dict = dict(target_list)

def import_csv():
    global opponents_ids
    opponents_ids = []
    with open('opponents_ids.csv') as f:
        for row in csv.reader(f):
            opponents_ids.append(row)
        opponents_ids = opponents_ids[0]
import_csv()



#
# send discord
#
import yaylib
import requests
from json import dumps
api = yaylib.Client()
headers = {'Content-Type': 'application/json'}
def send_discord_main(recipient_index, sender_id, text):
    webhook_url = target_list[recipient_index][1]
    sender = api.get_user(sender_id)
    main_content = {
        'username': f'{sender.nickname}({sender.id})',
        'avatar_url': sender.profile_icon_thumbnail,
        'content': text,
    }
    requests.post(webhook_url, dumps(main_content), headers=headers)
def send_discord_sub(recipient_id, sender_id, text, webhook_url):
    recipient = api.get_user(recipient_id)
    sender = api.get_user(sender_id)
    main_content = {
        'username': f'{sender.nickname}({sender_id})',
        'avatar_url': sender.profile_icon_thumbnail,
        'content': text,
        'embeds': [
            {
                'author': {
                    'name': f'{recipient.nickname}({recipient_id})',
                    'url': f'https://yay.space/user/{recipient_id}',
                    'icon_url': recipient.profile_icon_thumbnail,
                }
            }
        ],
    }
    requests.post(webhook_url, dumps(main_content), headers=headers)
def send_discord_log(text):
    main_content = {
        'username': f'log',
        # 'avatar_url': sender.profile_icon_thumbnail,
        'content': text,
    }
    requests.post(log_webhook, dumps(main_content), headers=headers)



#
# yaylib bot CLASS
#
from yaylib import Message
class MainBot(yaylib.Client):
    def __init__(self, intents, index):
        self.index = index
        super().__init__(intents=intents)
    def on_ready(self):
        print("ボットがオンラインになりました！")
    def on_message(self, message: Message):
        type = message.message_type
        str_sender_id = str(message.user_id)
        if type == "text":
            text = message.text
        elif type == "image" or type == "eternal_image":
            text = message.attachment
        elif type == "video" or type == "eternal_video":
            text = message.video_url
        elif type == "sticker":
            text = message.sticker.url
        elif type == "individual_call":
            text = message.conference_call.agora_channel
        send_discord_main(self.index, message.user_id, text)
        #監視者同士がチャットしてた場合はもう一人のチャットにも送信
        if str_sender_id in target_dict:
            send_discord_sub(target_list[self.index][0], message.user_id, text, target_dict[str_sender_id])
        #監視対象外の人からDMが来たらopponents_ids.csvに追加
        if str_sender_id not in opponents_ids and str_sender_id not in target_dict:
            csv_append(message.user_id)
            import_csv()
            new_thread(message.user_id)
            send_discord_log(f'監視対象が追加されました\nhttps://yay.space/user/{message.user_id}')
    def on_chat_room_delete(self, room_id):
        send_discord_main(self.index, 2 ,f"チャットルームが削除されました。ルームID: {room_id}")

class SubBot(yaylib.Client):
    def __init__(self, intents, id):
        self.id = id
        super().__init__(intents=intents)
    def on_ready(self):
        print("ボットがオンラインになりました！")
    def on_message(self, message: Message):
        type = message.message_type
        if type == "text":
            text = message.text
        elif type == "image" or type == "eternal_image":
            text = message.attachment
        elif type == "video" or type == "eternal_video":
            text = message.video_url
        elif type == "sticker":
            text = message.sticker.url
        elif type == "individual_call":
            text = message.conference_call.agora_channel
        #[その他チャンネル]に送るかどうかの処理
        if str(message.user_id) in target_dict:
            webhook_url = target_dict[str(message.user_id)]
        else:
            webhook_url = others_webhook
        send_discord_sub(self.id, message.user_id, text, webhook_url)
    # def on_chat_room_delete(self, room_id):
    #     send_discord_sub(self.id, 2 ,f"チャットルームが削除されました。ルームID: {room_id}", xxx)



#
# yaylib chat傍受botのインスタンス化とThreads
#
import threading
intents = yaylib.Intents.none()
intents.chat_message = True

main_bot = []
main_thread = []
for i in range(len(target_list)):
    main_bot.append(MainBot(intents, i))
    main_bot[i].set_ws_token(WSTokenGenerator.get_token(target_list[i][0]))
    main_thread.append(threading.Thread(target=main_bot[i].run))
    main_thread[i].start()

sub_bot = []
sub_thread = []
for i, id in enumerate(opponents_ids):
    sub_bot.append(SubBot(intents, id))
    sub_bot[i].set_ws_token(WSTokenGenerator.get_token(id))
    sub_thread.append(threading.Thread(target=sub_bot[i].run))
    sub_thread[i].start()


#
# new thread(監視対象を更に追加)
#
def new_thread(id):
    sub_bot.append(SubBot(intents, id))
    sub_bot[-1].set_ws_token(WSTokenGenerator.get_token(id))
    sub_thread.append(threading.Thread(target=sub_bot[-1].run))
    sub_thread[-1].start()

#
# 24時間毎にPythonを再起動
#
import subprocess

time.sleep(86400)
send_discord_log('shellが実行されました')
subprocess.call('python3 main.py', shell=True)