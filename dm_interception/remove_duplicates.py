import csv


# idsに opponents_ids.csvを代入
opp_ids = []
with open('opponents_ids.csv') as f:
    for row in csv.reader(f):
        opp_ids.append(row)
    opp_ids = opp_ids[0]

# idsの重複を削除
opp_ids = list(dict.fromkeys(opp_ids))



# target_listを取得
tar_ids = []
with open('target_list.csv') as f:
    for row in csv.reader(f):
        tar_ids.append(row)
tar_ids = [tar_id[0] for tar_id in tar_ids]

# target_listと重複したopponents_idを削除
for tar_id in tar_ids:
    try:
        opp_ids.remove(tar_id)
    except Exception:
        pass



# おれのサブ垢を削除(動作確認のため)
try:
    opp_ids.remove('8330622')
except Exception:
    pass

# opponents_list（自動で追加された監視対象）の人数を表示
print(f'opponents_list {len(opp_ids)}人')

# csvを整理したデータに更新
opp_ids = ','.join(opp_ids)
with open('opponents_ids.csv', 'w') as f:
    f.write(opp_ids)