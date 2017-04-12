# -*- coding: utf-8 -*-

# Импорт библиотек, необходимых для работы бота

import config
import telebot
import datetime
import feedparser
from openpyxl import load_workbook
import pymysql
from telebot import types

# Иниализация бота и импорт учительского пароля

bot = telebot.TeleBot(config.token)
teacher_pass = config.teacher_pass

# Загрузка расписания

wb = load_workbook(filename = '1.xlsx')
sheet_ranges = wb['1']

# Время начала уроков, классы, дни и словарь для рассылки

ll1 = datetime.time(2, 0, 0, 0,)
ll2 = datetime.time(8, 45, 0, 0)
ll3 = datetime.time(9, 45, 0, 0)
ll4 = datetime.time(10, 45, 0, 0)
ll5 = datetime.time(11, 45, 0, 0)
ll6 = datetime.time(12, 50, 0, 0)
ll7 = datetime.time(13, 55, 0, 0)
ll8 = datetime.time(14, 50, 0, 0)
ll9 = datetime.time(15, 35, 0, 0)

classes = {'5а' : 'C', '5б' : 'D', '5в' : 'E', '5г' : 'F', '5д' : 'G', '6а' : 'H', '6б' : 'I', 
           '6в' : 'J', '6г' : 'K', '7а' : 'L', '7б' : 'M', '7в' : 'N', '7г' : 'O', '7д' : 'P', 
           '8а' : 'Q', '8б' : 'R', '8в' : 'S', '8г' : 'T', '9а' : 'U', '9б' : 'V', '9в' : 'W', 
           '10.1' : 'X', '10.2' : 'Y', '10.3' : 'Z', '10.4' : 'AA', '10.5' : 'AB', '11.1' : 'AC',
           '11.2' : 'AD', '11.3' :'AE', '11.4' : 'AF'}

days = {0 : 'Понедельник: \n', 1 : 'Вторник: \n', 2 : 'Среда: \n', 3 : 'Четверг: \n', 4 : 'Пятница: \n'}

distr = {}


# In[6]:

# Кнопки меню (b = button, ch = char)

b_tt = types.KeyboardButton('Следующий Урок ' + chr(0x1F552))
b_news = types.KeyboardButton('Новости ' + chr(0x1F4C5))
b_links = types.KeyboardButton('Полезные Ссылки ' + chr(0x1F47E))
b_ads = types.KeyboardButton('Объявления ' + chr(0x1F4DD))
b_help = types.KeyboardButton('Помощь ' + chr(0x1F609))
b_cont = types.KeyboardButton('Поддержка ' + chr(0x2764))
b_lost = types.KeyboardButton('Потерянные Вещи' + chr(0x1F50E))
b_event = types.KeyboardButton('Мероприятия' + chr(0x23F0))
b_dist = types.KeyboardButton('Рассылка' + chr(0x2709))
b_parent = types.KeyboardButton('Родитель ' + chr(0x1F46A))
b_kid = types.KeyboardButton('Гимназист ' + chr(0x270D))
b_teacher = types.KeyboardButton('Учитель ' + chr(0x1F3EB))
b_more = types.KeyboardButton('Подробнее ' + chr(0x1F50E))
b_menu = types.KeyboardButton('Меню ' + chr(0x1F4CB))


# In[9]:

# Пользовательские клавиатуры (m = markup)

# Меню ученика
m_kid = types.ReplyKeyboardMarkup()
m_kid.row(b_tt, b_news)
m_kid.row(b_links, b_ads)
m_kid.row(b_cont)

# Меню учителя
m_teacher = types.ReplyKeyboardMarkup()
m_teacher.row(b_dist, b_news)
m_teacher.row(b_links, b_ads)
m_teacher.row(b_cont)

# Меню родителя
m_parent = types.ReplyKeyboardMarkup()
m_parent.row(b_news)
m_parent.row(b_ads)
m_parent.row(b_cont)

# Меню "Подробнее"
m_more = types.ReplyKeyboardMarkup()
m_more.row(b_more, b_menu)

# Меню "Объявления"
m_ads = types.ReplyKeyboardMarkup()
m_ads.row(b_event)
m_ads.row(b_lost)

# Меню регистрации
m_reg = types.ReplyKeyboardMarkup()
m_reg.row(b_kid)
m_reg.row(b_teacher)
m_reg.row(b_parent)

# Очистка клавиатуры
m_hide = types.ReplyKeyboardRemove()


# In[10]:

# Регистрация

# Учителя
def teacher_reg(message):
    if message.text == teacher_pass:
        conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("INSERT INTO main(chatid, status) VALUES ("+str(message.chat.id)+", 2);")
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, "Добро пожаловать в режим учителя!", reply_markup = m_teacher)
    else:
        bot.send_message(message.chat.id, "Пароль неверен!", reply_markup = m_reg)
        bot.register_next_step_handler(message, registration)
        
    
# Ученика
def kid_reg(message):
    clas = (message.text).lower()
    if len(clas) <= 4:
        if len(clas) == 3:
            clas = clas[0]+clas[2]
        if clas in classes:
            conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
            cur = conn.cursor()
            cur.execute("INSERT INTO main(chatid, status, class) VALUES ("+str(message.chat.id)+", 1, '"+
                        clas+"');")
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, "Спасибо за регистрацию! Добро пожаловать!", reply_markup = m_kid)
        else:
            bot.send_message(message.chat.id, "Неправильный формат ввода! Попробуйте еще раз. \n Пример: \n 9б, 10.1")
            bot.register_next_step_handler(message, kid_reg)
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода! Попробуйте еще раз. \n Пример: \n 9б, 10.1")
        bot.register_next_step_handler(message, kid_reg)


# Приветствие и выбор категории

def hello(message):
    bot.send_message(message.chat.id, "Добро Пожаловать! Чтобы продолжить, зарегистрируйтесь.", reply_markup = 
                     m_reg)
    bot.register_next_step_handler(message, registration)

def registration(message):
    if message.text == parent:
        bot.send_message(message.chat.id, "Приветствуем Вас в режиме родителя!", reply_markup = m_parent)
        
    elif message.text == teacher:
        bot.send_message(message.chat.id, "Введите пароль учителя!", reply_markup = m_hide)
        bot.register_next_step_handler(message, teacher_reg)
        
    elif message.text == kid:
        bot.send_message(message.chat.id, "Введите Ваш класс!", reply_markup = m_hide)
        bot.register_next_step_handler(message, kid_reg)
        
    else:
        bot.send_message(message.chat.id, "Выберите одну из категорий, предложенных в меню!", reply_markup =
                         m_reg)
        bot.register_next_step_handler(message, registration)


# In[ ]:

# Проверка авторизации

def check_reg(chatid):
    conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("SELECT status FROM main WHERE ChatID=" + str(chatid) + ";")
    out = ""
    for row in cur:
        out += str(row)
    cur.close()
    conn.close()
    if out == '':
        return 0
    else:
        return int(out)
    


# In[1]:

# Основной код (c = code)

# Новости
def c_news(message):
    out = 'Последние новости гимназии:'
    out += ent + ent
    d = feedparser.parse('http://gsg.mskobr.ru/data/rss/77/')
    for a in range (2):
        title = (d['entries'][a]['title'])
        link = (d['entries'][a]['link'])
        out += str(a+1) + '. ' + title + ent + link + ent
    bot.send_message(message.chat.id, out)
    
# "Подробнее" в расписании
def c_more(message):
    out = ''
    if message.text == '\n Подробнее ' + chr(0x1F50E):
        for day in range(4):
            out += days[day]
            for lesson in range (6):
                chartx = 1 + day * 8 + lesson+1
                chartx = str(chartx)
                tabl = charty + chartx
                if sheet_ranges[tabl].value == '':
                    out += '- \n'
                else:
                    out += sheet_ranges[tabl].value + '\n'
        bot.send_message(message.chat.id, out, reply_markup = m_kid)
    else:
        bot.send_message(message.chat.id, 'Выберите категорию!', reply_markup = m_kid)
    
# Расписание
def c_tt(message):
    conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("SELECT class FROM main WHERE ChatID=" + str(chatid) + ";")
    out = ""
    for row in cur:
        out += str(row)
    cur.close()
    conn.close()
    charty = classes[out]
    
    ddd = datetime.datetime.now()
    nowt = datetime.datetime.time(ddd)
    nowd = datetime.datetime.date(ddd)
    dday = datetime.datetime.weekday(nowd)

    if ll1 < nowt < ll2:
        les = 1
    elif ll2 < nowt < ll3:
        les = 2
    elif ll3 < nowt < ll4:
        les = 3
    elif ll4 < nowt < ll5:
        les = 4
    elif ll5 < nowt < ll6:
        les = 5
    elif ll6 < nowt < ll7:
        les = 6
    elif ll7 < nowt < ll8:
        les = 7
    elif ll8 < nowt < ll9:
        les = 8
    else:
        les = 0
    chartx = 1 + dday * 8 + les
    chartx = str(chartx)
    tabl = charty + chartx
    out = sheet_ranges[tabl].value
    if not (dday == 6 or dday == 5 or les == 0):
        bot.send_message(message.chat.id, 'Ваш следующий урок: \n' + out, reply_markup=markup10)
        bot.register_next_step_handler(message, c_more)
    else:
        bot.send_message(message.chat.id, "У вас больше нет сегодня уроков!", reply_markup=m_more)
        bot.register_next_step_handler(message, c_more)

# Полезные ссылки
def c_links(message):
    out = '**Образовательные интернет-ресурсы** \n https://www.udacity.com/ \n https://www.coursera.org/ \n https://www.edx.org/ \n welcome.stepik.org/ru \n https://foxford.ru/ \n \n **Олимпиады для школьников** \n https://reg.olimpiada.ru/ \n https://abitu.net/ \n https://it-edu.mipt.ru/ \n \n **Официальный сайт Гимназии** \n gsg.mskobr.ru/'
    bot.send_message(message.chat.id, out, parse_mode="Markdown")

# Добавление потерянной вещи
def c_lost(message):
    conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("INSERT INTO lost(item) VALUES ('"+message.text+"');")
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Объявление успешно добавлено!', reply_markup = m_teacher)
    
# Объявления, ч.2 (версия для учителей)
def c_ads2(message):
    if message.text == 'Мероприятия' + chr(0x23F0):
        sheet_ranges = wb['2']
        k = 1
        out = ''
        while k<=3:
            out += str(k)+'. '
            meropkor = 'A'+str(k+2)
            merop = sheet_ranges[meropkor].value
            merop = str(merop)
            out += merop + ', '
            meropkor = 'B' + str(k + 2)
            merop = sheet_ranges[meropkor].value
            merop = str(merop)
            out += merop + ' ' + ent
            meropkor = 'C' + str(k + 2)
            merop = sheet_ranges[meropkor].value
            merop = str(merop)
            out += merop + ent + ent
            k = k + 1
        sheet_ranges = wb['1']
        conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("SELECT status FROM main WHERE ChatID=" + str(chatid) + ";")
        out = ""
        for row in cur:
            out += str(row)
        cur.close()
        conn.close()
        
        if out == 1:
            bot.send_message(message.chat.id, out, reply_markup = m_kid)
        else:
            bot.send_message(message.chat.id, out, reply_markup = m_teacher)
    else:
        bot.send_message(message.chat.id, 'Здесь вы можете разместить объявление о нахождении чьей-то потерянной вещи. \n Чтобы продолжить, введите всю информацию о потерянной вещи в следующем сообщении. \n Чтобы выйти, отправьте "Выход".', reply_markup = m_hide)
        bot.register_next_step_handler(message, c_lost)
        
# Объявления, ч.2
def c_ads2(message):
    if message.text == 'Мероприятия' + chr(0x23F0):
        sheet_ranges = wb['2']
        k = 1
        out = ''
        while k<=3:
            out += str(k)+'. '
            meropkor = 'A'+str(k+2)
            merop = sheet_ranges[meropkor].value
            merop = str(merop)
            out += merop + ', '
            meropkor = 'B' + str(k + 2)
            merop = sheet_ranges[meropkor].value
            merop = str(merop)
            out += merop + ' ' + ent
            meropkor = 'C' + str(k + 2)
            merop = sheet_ranges[meropkor].value
            merop = str(merop)
            out += merop + ent + ent
            k = k + 1
        sheet_ranges = wb['1']
        conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("SELECT status FROM main WHERE ChatID=" + str(chatid) + ";")
        out = ""
        for row in cur:
            out += str(row)
        cur.close()
        conn.close()
        
        if out == 1:
            bot.send_message(message.chat.id, out, reply_markup = m_kid)
        else:
            bot.send_message(message.chat.id, out, reply_markup = m_teacher)
    else:
        conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("SELECT item FROM lost;")
        out = ""
        cnt = 1
        for row in cur:
            out += str(cnt) + '. ' + str(row) + '\n'
            cnt += 1
        cur.execute("SELECT status FROM main WHERE ChatID=" + str(chatid) + ";")
        clas = ""
        for row in cur:
            clas += str(row)
        cur.close()
        conn.close()
        
        if clas == 1:
            if out == '':
                bot.send_message(message.chat.id, 'Информации о потерянных вещах пока нет!', reply_markup = m_kid)
            else:
                bot.send_message(message.chat.id, out, reply_markup = m_kid)
        else:
            if out == '':
                bot.send_message(message.chat.id, 'Информации о потерянных вещах пока нет!', reply_markup = m_teacher)
            else:
                bot.send_message(message.chat.id, out, reply_markup = m_teacher)

# Объявления
def c_ads(message):
    bot.send_message(message.chat.id, "Выберите категорию!", reply_markup=m_ads)
    bot.register_next_step_handler(message, c_ads2)

# Объявления (версия для учителей)
def c_ads_t(message):
    bot.send_message(message.chat.id, "Выберите категорию!", reply_markup=m_ads)
    bot.register_next_step_handler(message, c_ads2_t)
    
# Контакты
def c_cont(message):
    out = 'Если вам есть, что сказать автору, Вы можете связаться со мной по этому никнейму в Telegram: \n @diveintodarkness \n Спасибо, что пользуетесь Помошником Гимназиста! '+chr(0x2764)
    bot.send_message(message.chat.id, out)
    
# Рассылки ч. 3
def c_dist3(message):
    conn = pymysql.connect(host='localhost', port=3306, user='bot', passwd='password', db='main', charset='utf8mb4')
    cur = conn.cursor()
    for adress in dist[message.chat.id]:
        cur.execute("SELECT chatid FROM main WHERE status="+adress+" OR class="+adress+";")
        for row in cur:
            bot.send_message(row[0], message.text)
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Сообщение успешно разослано!', reply_markup = m_teacher)

# Рассылки ч.2
def c_dist2(message):
    text = (message.text).lower()
    text = text.split(',')
    adresses = set()
    for adress in text:
        adress = adress.strip()
        if adress == 'учителя':
            adresses.add('2')
        elif adress == 'ученики':
            adresses.add('1')
        elif adress in classes and (not 1 in adresses):
            adresses.add(adress)
        else:
            bot.send_message(message.chat.id, 'Адресат ' + adress + ' не найден! \n Попробуйте ввести адресатов еще раз.')
            bot.register_next_step_handler(message, c_dist2)
            break
    distr[message.chat.id] = adresses
    bot.send_message(message.chat.id, 'Теперь введите рассылаемое сообщение.')
    bot.register_next_step_handler(message, c_dist3)
            
# Рассылки
def c_dist(message):
    bot.send_message(message.chat.id, 'Через запятую введите получателей сообщения. \n Возможные получатели: \n Учителя, родители, ученики, конкретный класс (10.1, 9б, 7в и т.д.)', reply_markup = m_hide)
    bot.register_next_step_handler(message, c_dist2)     

# Пользователские интерфейсы

# Интерфейс ученика
def c_kid(message):
    if 'Следующий Урок' in message.text:
        c_tt(message)
    elif 'Новости' in message.text:
        c_news(message)
    elif 'Полезные Ссылки' in message.text:
        c_links(message)
    elif 'Объявления' in message.text:
        c_ads(message)
    elif 'Поддержка' in message.text:
        c_cont(message)
    else:
        bot.send_message(message.chat.id, "Команда не опознанна!", reply_markup = m_kid)
        
# Интерфейс учителя
def c_teacher(message):
    if 'Рассылка' in message.text:
        c_dist(message)
    elif 'Новости' in message.text:
        c_news(message)
    elif 'Полезные Ссылки' in message.text:
        c_links(message)
    elif 'Объявления' in message.text:
        c_ads_t(message)
    elif 'Поддержка' in message.text:
        c_cont(message)
    else:
        bot.send_message(message.chat.id, "Команда не опознанна!", reply_markup = m_teacher)
        
# Интерфейс родителя
def c_parent(message):
    if 'Новости' in message.text:
        c_news(message)
    elif 'Объявления' in message.text:
        c_ads(message)
    elif 'Поддержка' in message.text:
        c_cont(message)
    else:
        bot.send_message(message.chat.id, "Команда не опознанна!", reply_markup = m_parent)

# Хендлер сообщений

@bot.message_handler(func=lambda message: (message.content_type == 'text'))
def all_messages(message):
    if message.text == '/start':
        hello(message)
    elif check_reg(message.chat.id) == 0:
        bot.send_message(message.chat.id, "Чтобы продолжить, зарегестрируйтесь.", reply_markup = m_reg)
        bot.register_next_step_handler(message, registration)
    elif check_reg(message.chat.id) == 1:
        bot.register_next_step_handler(message, c_kid)
    elif check_reg(message.chat.id) == 2:
        bot.register_next_step_handler(message, c_teacher)
    elif check_reg(message.chat.id) == 3:
        bot.register_next_step_handler(message, c_parent)

# Постоянный polling

if __name__ == '__main__':
    bot.polling(none_stop=True)

