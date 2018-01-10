from requests_oauthlib import OAuth1Session
import json,os
import urllib.request as req
import urllib

CK = 'zsjMLLwVGqjWtX8qIwKLfOOi1'                             # Consumer Key
CS = 'TdEqKJ7dEX0Bk3xbpQ78jcTTaSgAemNOUyuEP7P0yYDR17si0W'         # Consumer Secret
AT = '718046637377982464-bdsU4gpXawTtHdmN6SJKM2RJ3foruCP' # Access Token
AS = 'tWJUcCk38HBT6AN8nqJdPWvrqahf9FNSuMwzQVhYHCcZI'         # Accesss Token Secert

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=llimgfunbot"

# OAuth認証で POST method で投稿
twitter = OAuth1Session(CK, CS, AT, AS)
max_id = 0
gif_list = []
for i in range(10):
    print("------------" + str(i) + "------------")
    if not i == 0:
        params = {'max_id':max_id, 'count':200}
        request = twitter.get(url, params = params)
    else:
        params = {'count':200}
        request = twitter.get(url, params = params)
    tweet = json.loads(request.text)
    tweet_j = json.dumps(tweet, indent=4, separators=(',', ':'))
    max_id = tweet[199]['id']

    for tw in tweet:
        print(tw["extended_entities"]["media"][0]['video_info']['variants'][0]['url'])
        gif_list.append(tw["extended_entities"]["media"][0]['video_info']['variants'][0]['url'])

print("saving...:" + str(len(gif_list)) + "pic")

if not os.path.exists("image/gif"):
    os.mkdir("image/gif")

count = 0
for gif in gif_list:
    filename = "image/gif/" + gif[36:]
    print(str(count) + "/" + str(len(gif_list)) + " " + filename)
    if not os.path.exists(filename):
        req.urlretrieve(gif, filename)
    count += 1
