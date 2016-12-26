"""Chat bot for VK"""
import vk
from time import sleep
import random
import requests

my_id = 10607730

ox = [
'Говно', 'Залупа', 'Пенис', 'Хер',
'Давалка', 'Хуй', 'Блядина',
'Головка', 'Шлюха', 'Жопа', 'Член',
'Еблан', 'Петух', 
'Мудила...',
'Рукоблуд', 'ссанина',
'Очкоблядун', 'вагина',
'Сука', 'ебланище', 'влагалище', 'пердун', 'дрочила',
'Пидор', 'пизда',
'Туз', 'малафья',
'Гомик', 'мудила', 'пилотка', 'манда',
'Анус', 'вагина', 'путана', 'педрила',
'Шалава', 'хуила', 'мошонка', 'елда',
'Раунд!'
]

ans = [
 'Спасение России в том, чтобы талантливые ее люди друг другу не мешали, а помогали бы друг другу.',
 'Тебе веселоесело?)', 'Нажитое от общества должно быть возвращено обществу.', 'Есть лекарство от сна. Называется «чувство времени».', 
 'Бывало, я начинала мудрствовать по пустякам и находила миллион причин сомневаться в самой себе.', 
 'Всякий влюбленный слегка ненормален. Любовь вообще безумна. Это некая форма социально принятого сумасшествия.',
 'Чем ты выше, тем больше нужно заботиться о справедливости.', 
 'Шатается земля, как пьяный, и качается, как колыбель, и беззаконие ее тяготеет на ней; она упадет, и уже не встанет.', 
 'Если все, кого обездолила война, будут мстить, у нас будет уйма мстителей с обеих сторон.', 
 'Характер и личная сила — вот единственные достойные приобретения.',
 'Любопытствуй, а не критикуй.', 'Я считаю, что мужчина всегда должен быть готов нести ответственность за свои поступки.'
 ]

def vk_round(id_):
    for i in ox:
        api.messages.send(user_id=id_, message=i)
        print(i)
        sleep(3)

def bot_req(bot_answer):
    """Sending massage to Bot"""
    url = 'https://xu.su/api/send'

    question = {"uid":"f969c58e-fc7a-435d-9f2a-dd55fb534824","bot":"old", "text": bot_answer}

    headers = {
    'Accept':'application/json',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection':'keep-alive',
    'Content-Length':'72',
    'Content-Type':'application/json',
    'Host':'xu.su',
    'Origin':'https://xu.su',
    'Referer':'https://xu.su/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    }

    r = requests.post(url, params=headers, data=question)

    return r.json()["text"]



# Open file token or log\pass login
try:
    with open("Token", "r") as f:
        token = f.read()
        session = vk.Session(access_token=token)
except Exception:
    log = input("Login: ")
    pswrd = input("Password: ")
    session = vk.AuthSession(app_id=5377227, user_login=log, user_password=pswrd, 
                         scope="friends,photos,audio,video,docs,notes,pages,status,wall,groups,messages,notifications,offline")
    token = session.get_access_token()
    print(token)
    with open("Token", "w") as f:
        f.write(token)


api = vk.API(session)
# welcome
info = api.users.get()
print("Привет, " + info[0]["first_name"] + "! Пошалим?")

# Cheking users massages and answers 
while True:
    mes = api.messages.get(count=1)
    print("От {us}; Статус: {st}; Пишет:{wr}".format(us=api.users.get(user_ids=mes[1]["uid"])[0]["first_name"], 
                                                     wr=mes[1]["body"], 
                                                     st=mes[1]["read_state"]))
    
    if mes[1]["uid"] != my_id and mes[1]["read_state"] == 0 and mes[1]["body"] != "Раунд":
        bot_mes = bot_req(mes[1]["body"])
        print("Ответ:", bot_mes)
        try:
            api.messages.send(user_id=mes[1]["uid"], message=bot_mes)   #"{}".format(random.choice(ans)))
        except Exception:
            api.messages.send(user_id=mes[1]["uid"], message=bot_mes)  #"{}".format(random.choice(ans)))
        api.messages.markAsRead(message_ids=mes[1]["mid"])

    elif mes[1]["body"] == "Раунд" and mes[1]["read_state"] == 0:
        vk_round(mes[1]["uid"])
        api.messages.markAsRead(message_ids=mes[1]["mid"])
    
    sleep(15)
