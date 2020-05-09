# [設定]
# シルバーtier4ポイント0をスタート地点とする。
#
# ブロンズ帯は負けてもポイント下がらないため、
# 勝率0％でなければシルバーまでは行けるので、シミュレーションから除外する。
# 
# 試したことないから分からないけど、
# シルバーでいくら負けてもブロンズには下がらないものとする。

import random

# 設定

need_point = 5     # リミテでは5ポイント貯めるとtierアップ
max_tier = 4       # tierは1,2,3,4の4個
max_rank = 4       # 1:シルバー 2:ゴールド 3:プラチナ 4:ダイアモンド
barrier_turn = 3   # ランクアップ直後に負けたもランク落ちない期間
max_iter = 10000   # 最大対戦回数
win_percent = 0.48 # 勝率
max_sim = 10000    # シミュレーション回数

sim_count = 0
match_num_for_mythic = list()   # 1回のシミュレーションで、ミシックになるために何回対戦が必要だったかを記録

while sim_count < max_sim:
    sim_count += 1
    count = 0
    point = 0
    tier = 4
    rank = 1
    barrier = 0
    
    while count < max_iter:
        count+=1
        rand = random.random()

        result = "lose"
        if rand <= win_percent:
            result = "win"

        # 勝った時の処理
        if result == "win":
            if rank == 1:
                point += 2 # シルバーだけは勝つと2ポイント
            else:
                point += 1
            if point >= need_point:
                tier -= 1
                point = 0
                barrier = barrier_turn + 1 # イテレーションの最後でマイナスするんで1を足す必要あり
                if tier == 0:
                    tier = max_tier
                    rank += 1
                    if rank > max_rank:
                        match_num_for_mythic.append(count)
                        break

        # 負けたときの処理
        if result == "lose":
            # シルバーtier4ポイント0なら何も起こらない
            if not(rank == 1 and tier == max_tier and point == 0):
                # ポイント0かつバリア中なら何も起こらない
                if not(point == 0 and barrier > 0):
                    point -= 1
                    if point < 0:
                        tier += 1
                        point = need_point - 1
                        if tier > max_tier:
                            rank -=1
                            tier = max_tier


        # デバッグ用のprint
        #print(count,rank,tier,point,result)

        barrier = max(barrier -1 , 0) # バリアを縮ませる

print("mean",sum(match_num_for_mythic)/len(match_num_for_mythic))
print("failure",(max_sim-len(match_num_for_mythic))/max_sim)


