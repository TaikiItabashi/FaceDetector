import urllib.request as req
import urllib
import json, os

#print(json.dumps(idols, indent=4))

#カードの一覧を取得する
#取得できるリストは10件ずつとなっていて、リンク形式なので再帰的に関数を呼び出す
#取得した一覧はローカルファイルに出力
#二度目以降はファイルから読み出す
#戻り値：JSON(dic?)形式のカード一覧
card_lists = []
def get_lists(url, target):
    global card_lists
    local_path = target + "_lists.json"                  #ローカルファイルのパス
    if not os.path.exists(local_path):              #ローカルにファイルが存在しない場合
        print(url)
        res = req.urlopen(url)
        lists = json.load(res)
        if lists["next"] != None:                   #次のリストがあるとき
            next_link = lists["next"]
            for li in lists["results"]:
                card_lists.append(li)
            get_lists(next_link, target)                #再帰
        else:                                       #次のリスト
            for li in lists["results"]:
                card_lists.append(li)
            f = open(local_path, 'w')
            json.dump(card_lists, f)
            return card_lists
    else:                                           #ローカルにファイルが存在する場合
        f = open(local_path, 'r')
        card_lists = json.load(f)
        return card_lists

#カード画像を取得する
# target == "round" :: ラウンド画像
# target == "card"  :: カード画像
def get_image(dir_path, keyword, target, search_type):
    if not os.path.exists(dir_path): os.mkdir(dir_path)
    API = "http://schoolido.lu/api/" + target + "/"
    card_lists = get_lists(API, target)
    result_lists = []
    if target == "card":
        for li in card_lists:       #キーワードで検索
            if li['idol']['name'] == keyword:
                result_lists.append(li)
        for li in result_lists:     #画像を保存
            if target == "round":
                #覚醒前
                if not li['round_card_image'] is None:
                    image_url = "http:" + li['round_card_image']
                    save_path = dir_path + str(li["id"]) + ".jpg"
                    print(save_path)
                    if not os.path.exists(save_path):
                        req.urlretrieve(image_url, save_path)
                #覚醒後
                if not li['round_card_idolized_image'] is None:
                    image_url = "http:" + li['round_card_idolized_image']
                    save_path = dir_path + "i" + str(li["id"]) + ".jpg"
                    print(save_path)
                    if not os.path.exists(save_path):
                        req.urlretrieve(image_url, save_path)
            elif target == "card":
                if not li['transparent_image'] is None:
                    image_url = "http:" + li['transparent_image']
                    save_path = dir_path + str(li["id"]) + ".jpg"
                    print(save_path)
                    if not os.path.exists(save_path):
                        req.urlretrieve(image_url, save_path)
                if not li['transparent_idolized_image'] is None:
                    image_url = "http:" + li['transparent_idolized_image']
                    save_path = dir_path + "i" + str(li["id"]) + ".jpg"
                    print(save_path)
                    if not os.path.exists(save_path):
                        req.urlretrieve(image_url, save_path)

    #CDジャケット
    elif target == "songs":
        for li in card_lists:       #キーワードで検索
            if not li['main_unit'] == "Aqours":
                result_lists.append(li)
        for li in result_lists:
            if not li['image'] is None:
                parse = urllib.parse.quote_plus(li['image'])
                image_url = "http://" + parse[6:20] + "/" + parse[23:28] + "/" + parse[31:]
                save_path = dir_path + str(li["id"]) + ".jpg"
                print(li['name'])
                print(save_path)
                if not os.path.exists(save_path):
                    req.urlretrieve(image_url, save_path)

#main関数
name = [
    "Kousaka Honoka", "Sonoda Umi", "Minami Kotori",
    "Nishikino Maki", "Koizumi Hanayo", "Hoshizora Rin",
    "Ayase Eli", "Toujou Nozomi", "Yazawa Nico"
]

#ジャケットの取得
path = "image/" + "music" + "/"
get_image(path, "µ\'s", "songs", "name")

#キャラごとに分別
for charname in name:
    path = "image/" + charname + "/"
    get_image(path, charname, "card", "name")
    # get_image(path, charname, "name")
