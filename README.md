# yaylib-scripts
Yaylib使って作ったやつのガラクタコレクション

## ディレクトリ構成と機能

### `dm_interseption/`
DM（ダイレクトメッセージ）を傍受(盗聴)するためのモジュールです  
指定したユーザーをDMを監視し、その人にDMを送った人も自動で監視対象に追加します  
運営に報告済みなので過去の遺産(?)です

### `notify_new_users/`
サークルの新規参加者・脱退者を検出し、通知を行う機能を持っています  
定期的に参加メンバーを比較し、差分をDiscordに送信  
新規参加者にYay!内でWelcomeメッセージを送信

### `online_log/`
指定したユーザーのonline、offline通知をDiscordに送信

### `block_notifire/`
あなたをブロックしたユーザーを通知します