"""Chat bot for VK"""

from time import sleep
import random

import requests
import vk

app_id_ = "id_РїСЂРёР»РѕР¶РµРЅРёСЏ"


def bot_req(bot_question):
    """Send massage to Bot"""
    url = 'https://xu.su/api/send'

    question = {"uid": "f969c58e-fc7a-435d-9f2a-dd55fb534824",
                "bot": "old", "text": bot_question}

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Length': '72',
        'Content-Type': 'application/json',
        'Host': 'xu.su',
        'Origin': 'https://xu.su',
        'Referer': 'https://xu.su/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0)\
                       Gecko/20100101 Firefox/47.0',
    }

    r = requests.post(url, params=headers, data=question)

    return r.json()["text"]


# Log in by token or log\pass auth
try:
    with open("Token", "r") as f:
        token = f.read()
        session = vk.Session(access_token=token)

except Exception:
    while True:
        log = input("Login: ")
        pswrd = input("Password: ")
        try:
            session = vk.AuthSession(app_id=app_id_,
                                     user_login=log,
                                     user_password=pswrd,
                                     scope="friends,photos,audio,video,docs,\
                                            notes,pages,status,wall,groups,\
                                            messages,notifications,offline")

        except Exception:
            print("РќРµРІРµСЂРЅРѕРµ СЃРѕС‡РµС‚Р°РЅРёРµ Р»РѕРіРёРЅ/РїР°СЂРѕР»СЊ")

        else:
            token = session.get_access_token()
            with open("Token", "w") as f:
                f.write(token)
            break


api = vk.API(session)

# welcome
info = api.users.get()
print("РџСЂРёРІРµС‚, " + info[0]["first_name"] + "! РџРѕС€Р°Р»РёРј?")

# Check user's massage and answer
while True:
    mes = api.messages.get(count=1)

    if mes[1]["read_state"] == 0:
        print("РћС‚ {us}: {wr}".format(us=api.users.get(
                                     user_ids=mes[1]["uid"])[0]["first_name"],
                                     wr=mes[1]["body"]))

        bot_mes = bot_req(mes[1]["body"])
        print("РћС‚РІРµС‚:", bot_mes)

        try:
            api.messages.send(user_id=mes[1]["uid"], message=bot_mes)
        except Exception:
            api.messages.send(user_id=mes[1]["uid"], message=bot_mes)
        finally:
            api.messages.markAsRead(message_ids=mes[1]["mid"])

sleep(3)
