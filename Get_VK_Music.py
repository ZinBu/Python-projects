
import urllib.request
from tkinter import *
from tkinter.ttk import Button, Entry, Label, Scrollbar, Progressbar, Style, Frame
import json
import os

import vk


class Main:
    """Основной класс"""
    
    def __init__(self, root):
        
        Gui(root).try_engage()    # запускаемся, пытаемся автоматически авторизироваться
      

class Logic():
    """ Основная логика приложения """
    
    app_id_ = 5377227
      

    def try_engage(self):   
        """ Попытка автоматической авторизации """   
        try:
            with open("Memory", 'r') as f:
                token = json.load(f)["token"]
                self.auth_token(token)
                self.welcome()

        except Exception as e:
            print(e)
            pass


    def welcome(self):
        """ Приветствие """

        info = api.users.get()
        self.label["text"] = "Привет, " + info[0]["first_name"] + "!"
        self.but3["state"] = "active"
        self.but4["state"] = "active"
        self.track_count["state"] = "active"


    def auth_log(self, log, pswrd):
        """ Авторизация по логину/пассу """

        global api
        session = vk.AuthSession(app_id=self.app_id_, user_login=log, user_password=pswrd, scope="audio, offline")
        token = session.get_access_token()
        api = vk.API(session)

        with open("Memory", 'w') as f:
            json.dump({"token":token} , f)



    def auth_token(self, token):
        """ Авторизация по токену """

        global api
        session = vk.Session(access_token=token)
        api = vk.API(session)


    def log_pass(self):
        """ Обработчик нажатия кнопки ввод лог/пасса """

        try:
            self.auth_log(self.login.get(), self.psw.get())
            self.welcome()

        except Exception:
            self.label["text"] = "Неверный логин/пароль" 

        finally:
            self.lwin.destroy()


    def music_but(self):
        """ Обработчик кнопки получения списка музыки """

        count = self.track_count.get()
        self.get_music(count)
        self.music_info()


    def music_info(self):
        """ Вывод списка музыки в UI """

        self.text["state"] = "normal"
        self.text.delete('1.0', END)
        count = 0
        title = "-"*40+" Список музыки "+"-"*40
        self.ins(title)
        for i in music:
            count += 1
            url = i["url"]
            track_name = "{} - {}".format(i["artist"], i["title"])
            form = str(count) + ". " + track_name            
            self.ins(form)

        self.text["state"] = "disabled"


    def get_music(self, count):
        """ Получение списка музыки """

        global music
        music = api.audio.get(count=count)


    def download(self, url, name):
        """ Скачивание трека по ссылке """

        # проверка папки и ее создание
        if "Downloaded" in os.listdir():
            pass

        else:
            os.mkdir("Downloaded")

        with open("Downloaded/"+name+".mp3", "wb") as f:
            track = urllib.request.urlopen(url).read()
            f.write(track)


    def start_download(self):
        """ Загрузка выбранной музыки """
    
        # создание прогресс бара
        self.progress_bar = Progressbar(self.frame, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress_bar.place(x=5, y =400)

        try:
            # задание размерности прогресс бара
            self.progress_bar['maximum'] = len(music)
            self.text["state"] = "normal"
            self.text.delete('1.0', END)
            self.ins("Идет скачивание...\n")
        
            for i in music:
                url = i["url"]
                track_name = "{} - {}".format(i["artist"], i["title"])
                form = "Идет скачивание: "+ track_name
                self.ins(form)
                root.update()
                
                self.download(url, track_name)
                self.ins("Успешно скачено\n")
                self.progress_bar.step()        # увеличиваем значение прогресс бара на шаг
                root.update()

        except Exception:
            self.ins("\nКакая-то ошибка!!!")

        else:
            self.ins("\n\nВся музыка скачена")
            self.text["state"] = "disable"
        
        self.progress_bar.destroy()


    def ins(self, track):
        """ Вставка текста в текстовое поле """

        self.text.insert(END, track+"\n")


class Gui(Logic):
    """ Интерфейс """
    
    icon = "icon.ico"
    theme_flag = 'blue'

    def __init__(self, root):
        root.title('Get Music')
        root.geometry('800x450+500+300')        # ширина, высота, положение(x, y)
        root.resizable(False, False)            # размер окна не может быть изменён
        try:
            root.iconbitmap(self.icon)
        except Exception:
            pass
        
        # настройка стилей
        self.style = Style()
        self.style.theme_use('default')   # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        
        try:
            with open("Memory_theme", 'r') as f:
                theme = json.load(f)["theme"]
                self.theme_flag = theme

                if theme == 'blue':
                    self.use_theme_1()
                elif theme == 'dark':
                    self.use_theme_2()

        except Exception:
            self.use_theme_1()

        # установка фреймов
        self.panel_frame = Frame(root, heigh="50", style="My.TFrame")
        self.panel_frame.pack(side='top', fill='x')

        self.frame = Frame(root, heigh="375").pack(side='top', fill='x')

        self.status = Frame(root, heigh="50", style="My.TFrame").pack(side='bottom', fill='x')

        self.label = Label(self.panel_frame, text="Вы не авторизированы", style="Panel.TLabel")
        self.label.place(x=600, y =13)

        self.label_frame = Label(self.frame, text="Сколько последних\nзаписей показать?",
                                             style="Frame.TLabel").place(x=20, y =70)


        self.but1 = Button(self.panel_frame, text="Вход", command=self.login_window).place(x=25, y =13)

        self.but3 = Button(self.frame, text="Список", command=self.music_but, state="disabled")
        self.but3.place(x=25, y =150)

        self.but4 = Button(self.frame, text="Скачать", state="disabled", command=self.start_download)
        self.but4.place(x=25, y =300)

        self.text = Text(self.frame, height=18, width=75, font='Calibri 11', wrap=WORD, state="disabled")
        self.text.place(x=250, y =90)

        self.text_name = Label(self.frame, text="Список музыки",
                                           style="Frame.TLabel").place(x=460, y =60)

        # установка скроллбара в текст
        self.scrollbar = Scrollbar(self.text, orient=VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(x=700, y =30)
        
        # проверочный прогресс бар
        # self.progress_bar = Progressbar(self.frame, orient=HORIZONTAL, length=200, mode='determinate')
        # self.progress_bar.place(x=5, y =400)
        # self.progress_bar.start()

        # количество треков, которое необходимо показать
        self.track_count = Entry(self.frame, width=5, state="disabled")
        self.track_count.place(x=180, y =90)

        self.panel_frame.bind('<3>', self.change_theme) # клик ПКМ по верхнему фрейму меняет стиль оформления

   
    def login_window(self):
        """ Окно авторизации """

        # выбор стиля окна в зависимости от основного
        if self.theme_flag == "blue":
            bg = "#94b9ff"
            fr_log = "white"
            fr_pass = "#575757"

        elif self.theme_flag == "dark":
            bg = "#2c3d4f"
            fr_log = "white"
            fr_pass = "white"

        self.lwin = Toplevel(root, background=bg)
        try:
            self.lwin.iconbitmap(self.icon)
        except Exception:
            pass
        self.lwin.grab_set()                    # устанавливаем фокус на окно
        self.lwin.title('Авторизация')
        self.lwin.geometry('500x200+600+300')   # ширина, высота, положение(x, y)
        self.lwin.resizable(False, False)       # размер окна не может быть изменён
        
        self.label_log = Label(self.lwin, text="Логин",
                               background=bg, foreground=fr_log,
                               font='Calibri 12').place(x=60, y =45)

        self.label_pass = Label(self.lwin, text="Пароль",
                                background=bg, foreground=fr_pass,
                                font='Calibri 12').place(x=60, y =95)

        # поле ввода логина
        self.login = Entry(self.lwin, width=30)
        self.login.place(x=180, y =50)

        # поле ввода пароля с сокрытием символов
        self.psw = Entry(self.lwin, width=30, show='*')
        self.psw.place(x=180, y =100)

        self.but_enter = Button(self.lwin, text="Вход", command=self.log_pass).place(x=210, y =150)


    def change_theme(self, event):
        """ Смена стиля окна по клику """ 

        if self.theme_flag == 'blue':
            self.use_theme_2()
            self.theme_flag = 'dark'

        elif self.theme_flag == 'dark':
            self.use_theme_1()
            self.theme_flag = 'blue'

        # сохраняем тему для загрузки при следующем открытии
        with open("Memory_theme", 'w') as f:
            json.dump({"theme":self.theme_flag} , f) 


    def use_theme_2(self):
        """ Стиль 2 """

        orange = '#f59d2a'
        dark_light = "#34495d"
        yellow = '#ee7738'
        dark = '#2c3d4f'

        bg_color_frame = dark
        bg_color_main = orange        

        # кнопки 
        self.style.configure("TButton", background=yellow, padding=2, width=10, relief="ridge")  
      
        self.style.configure("Horizontal.TProgressbar", background=bg_color_main)  # прогресс бар

        # фреймы
        self.style.configure("My.TFrame", background=bg_color_main)  
        self.style.configure("TFrame", background=bg_color_frame)       

        # лэйблы
        self.style.configure("Panel.TLabel", background=bg_color_main, foreground="black", font='Calibri 12')
        self.style.configure("Frame.TLabel", background=bg_color_frame, foreground="white", font='Calibri 12')


    def use_theme_1(self):
        """ Стиль 1 """

        bg_color_frame = "white"
        bg_color_main = '#059fff'

        # кнопки 
        self.style.configure("TButton", background="#94b9ff", padding=2, width=10, relief="ridge")  
        
        self.style.configure("Horizontal.TProgressbar", background=bg_color_main)  # прогресс бар

        # фреймы
        self.style.configure("My.TFrame", background=bg_color_main)  
        self.style.configure("TFrame", background=bg_color_frame)       

        # лэйблы
        self.style.configure("Panel.TLabel", background=bg_color_main, foreground="white", font='Calibri 12')
        self.style.configure("Frame.TLabel", background=bg_color_frame, foreground="black", font='Calibri 12')


if __name__ == '__main__':
    root = Tk()
    obj = Main(root)
    root.mainloop()