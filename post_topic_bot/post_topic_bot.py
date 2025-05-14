import time
import random
import json

import yaylib


email = ""
password = ""

def post(str):
    while True:
        try:
            bot = yaylib.Client()
            bot.login(email, password)
            bot.create_post(str)
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3600) # 1時間待機

def post_topic():
    with open('topics.json', 'r') as f:
        topics = json.load(f)

    unposted_topics = [t for t in topics if not t.get('posted', False)]

    # 投稿するトピックがある場合
    if unposted_topics:
        # ランダムにトピックを選択して投稿
        selected = random.choice(unposted_topics)
        post(selected['description'])

        # 投稿したトピックのpostedをtrueにする
        for topic in topics:
            if topic['description'] == selected['description']:
                topic['posted'] = True
                break
    # 投稿するトピックがない場合
    else:
        print("すべてのトピックが投稿されました")
        post("すべてのトピックが投稿されました")
        # すべてのトピックが投稿されたので、postedをfalseに戻す
        for topic in topics:
            topic['posted'] = False
    # 更新されたtopicsを保存
    with open('topics.json', 'w') as f:
        json.dump(topics, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    # 3時間ごとに投稿
    while True:
        post_topic()
        time.sleep(3600 * 3)
