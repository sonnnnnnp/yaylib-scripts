import random
import time

from bs4 import BeautifulSoup
import requests

import yaylib

email = ""
password = ""

with open('5000-words.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

def post(str):
    while True:
        try:
            bot = yaylib.Client()
            bot.login(email, password)
            bot.create_post(str)
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1800)  # 30分待機

def get_meaning(word):
    url = f"https://ejje.weblio.jp/content/{word}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    element = soup.find('span', class_=['content-explanation', 'ej'])
    jp_meaning = element.text.strip()
    return jp_meaning


if __name__ == "__main__":
    # 1時間ごとに投稿
    while True:
        en_word = random.choice(lines)
        jp_meaning = get_meaning(en_word)
        post(f"【 {en_word} 】\n{jp_meaning}")
        time.sleep(3600)
