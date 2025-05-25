# 2025/5/23

EMAIL = ''
PASSWORD = ''

import math
import requests

class PriceFetcher:
    BTC_API_URL = 'https://coincheck.com/api/ticker'
    GMO_API_URL = 'https://forex-api.coin.z.com/public/v1/ticker'

    @classmethod
    def btc_jpy(cls):
        response = requests.get(cls.BTC_API_URL)
        if response.status_code != 200:
            print(f'エラーが発生しました。ステータス：{response.status_code}, メッセージ：{response.text}')
            return None
        data = math.floor(response.json()['last'])
        return f'{data:,}'

    @classmethod
    def usd_jpy(cls):
        response = requests.get(cls.GMO_API_URL)
        if response.status_code != 200:
            print(f'エラーが発生しました。ステータス：{response.status_code}, メッセージ：{response.text}')
            return None
        data = float(response.json()['data'][0]['ask'])
        return f'{data:.3f}'


from PIL import Image, ImageDraw, ImageFont

class ImageGenerator:
    IMAGE_SIZE = (1200, 600) # 画像サイズ
    BACKGROUND_COLOR = (255, 255, 255) # 背景色
    TEXT_COLOR = (0, 0, 0) # テキスト色
    FONT_PATH = '/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc'  # macOSのフォントパス
    BITCOIN_LOGO_PATH = 'assets/bitcoin.jpg'  # ビットコインのロゴパス
    USDJPY_LOGO_PATH = 'assets/usdjpy.jpg'  # USD/JPYのロゴパス
    
    @classmethod
    def generate_image(cls, btcjpy_price, usdjpy_price):
        # 背景画像を生成
        image = Image.new('RGB', cls.IMAGE_SIZE, cls.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)

        # ロゴ画像を貼り付け
        bitcoin_img = Image.open(cls.BITCOIN_LOGO_PATH)
        usdjpy_img = Image.open(cls.USDJPY_LOGO_PATH)
        bitcoin_img = bitcoin_img.resize((300, 300))
        usdjpy_img = usdjpy_img.resize((300, 300))
        image.paste(bitcoin_img, (0, 0))
        image.paste(usdjpy_img, (0, 300))

        # テキストを描画
        font = ImageFont.truetype(cls.FONT_PATH, 110)
        draw.text((360, 105), btcjpy_price, fill=cls.TEXT_COLOR, font=font)
        font = ImageFont.truetype(cls.FONT_PATH, 130)
        draw.text((380, 385), usdjpy_price, fill=cls.TEXT_COLOR, font=font)

        return image


from datetime import datetime
import time

class TimeUtil:
    @staticmethod
    def get_current_time():
        now = datetime.now()
        return now.strftime('%Y/%m/%d %H:%M:%S')
    @staticmethod
    def wait_until_next_hour():
        now = datetime.now()
        # 次の00分までの秒数を計算
        seconds_until_next_hour = (60 - now.minute) * 60 - now.second
        time.sleep(seconds_until_next_hour)


import yaylib

def main():
    bot = yaylib.Client()
    bot.login(EMAIL, PASSWORD)
    while True:
        btc = PriceFetcher.btc_jpy()
        usd = PriceFetcher.usd_jpy()

        image = ImageGenerator.generate_image(f'{btc}円', f'{usd}円')
        image.save('tmp/post.jpg')

        image_paths = ['tmp/post.jpg']
        
        image_type = yaylib.ImageType.POST
        attachments = bot.upload_image(image_paths, image_type)

        bot.create_post(
            f"{TimeUtil.get_current_time()} 現在の価格",
            attachment_filename=attachments[0].filename,
        )

        TimeUtil.wait_until_next_hour()

if __name__ == '__main__':
    main()