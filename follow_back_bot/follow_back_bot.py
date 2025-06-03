# 2025/6/4 5:17
# フォロバbot
# 10分で書き上げた挙句動作テストもしてないけど多分動く
import time
import yaylib

email = ''
password = ''

bot = yaylib.Client()
bot.login(email, password)

followed_user_ids = []

while True:
    try:
        # 全種類の通知を読み込む
        activities = bot.get_merged_activities().activities
    except Exception as e:
        time.sleep(60)
        continue
    
    for activity in activities:
        # follow通知以外はスルー
        if not activity.type == 'follow':
            continue
        # 最新のフォロー通知のユーザーをフォロー
        for follower in activity.followers:
            # フォロー済の場合はスルー
            if follower.id in followed_user_ids:
                continue
            try:
                # フォローする
                response = bot.follow_user(follower.id)
                if response.result == 'success':
                    followed_user_ids.append(follower.id)
                    print(f'フォローを返しました: {follower.nickname}({follower.id})')
                else:
                    print(f'フォロー返し中にエラーが発生しました: {follower.nickname}({follower.id})\n{response}')
            except Exception as e:
                print(f'フォロー返し中にエラーが発生しました: {follower.nickname}({follower.id})\n{e}')
        time.sleep(30)