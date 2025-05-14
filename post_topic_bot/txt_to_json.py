# topic.txt を読み込み、JSON 形式に変換するスクリプト

import json

input_file = 'topics.txt'
output_file = 'topics.json'

with open(input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

topics = []

for i, line in enumerate(lines, start=1):
    topics.append({
        "id": i,
        "posted": False,
        "description": line.replace('\\n', '\n')
    })

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(topics, f, ensure_ascii=False, indent=4)

print(f"{len(topics)} 件のトピックを JSON に変換しました。")