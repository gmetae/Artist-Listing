#   ver. 1.0

import re
import os
import sys
import shutil
from datetime import datetime
from itertools import groupby
import requests
from lxml import html

#   Загружаем данные о наблюдаемых исполнителях с www.album-info.ru
#   Авторизация
url = "http://www.album-info.ru/Auth.aspx"
sess = requests.Session()
req = sess.post(url, data = {'ctl00$CPH$tbName':'gmetae', 'ctl00$CPH$tbPassword':'H6aIk)7nsg^UL7S4*1|5', '__EVENTTARGET':'ctl00$CPH$btnOK'})
req = sess.get('http://www.album-info.ru/my.aspx')
if re.search(u'Мои исполнители', req.text):
    print ("Авторизация на www.album-info.ru: Успешно!")
else:
    print ("Авторизация на www.album-info.ru: Ошибка!")

#   Парсим полученую страницу с исполнителями
tree = html.fromstring(req.text)
site_artist_list = tree.xpath('//div[@class="artistBlock"]/text()')
for item in range(len(site_artist_list)):
    site_artist_list[item] = site_artist_list[item].lower() + '\r'

#   Найстройки для чтения из файлов выгрузки
album_list_folder = "C:\\Users\\gmetae\\OneDrive\\Documents\\Music\\Album lists\\"
out_folder = "C:\\Users\\gmetae\\OneDrive\\Documents\\Music\\LIST\\"
album_list_files = os.listdir(path = album_list_folder)
artist_list = []
now_time = datetime.now()        #  Текущая дата со временем

#   Проходим по всем файлам в папке
for file in album_list_files:
    
    if not os.path.exists(album_list_folder + file):
        print("Файл %s не существует" % album_list_files[i])
        sys.exit(0)
    
    #   Открываем каждый файл в папке
    list_file = open(album_list_folder + file, 'rb')
    list_file_data = list_file.read()
    list_file.close()
    list_data = str(list_file_data.decode("utf-8"))         #   перекодируем в utf-8

    #   Ищем все вхождения поля Artist в файле выгрузки
    artist_list = artist_list + re.findall(r'Artist\s+:\s(.+)', list_data)

artist_list.sort()                                          #   сортируем список
new_artist_list = [el for el, _ in groupby(artist_list)]    #   Убираем дубли

#   Ищем совпадающих исполнителей в выгрузке с сайта
#   Найденый помечаем +
found_artist = 0
for item in range(len(new_artist_list)):
    new_str = new_artist_list[item]
    new_str = new_str.replace("é", "e")
    new_str = new_str.replace("á", "a")
    new_str = new_str.replace("ø", "o")
    new_str = new_str.replace("ë", "e")
    new_str = new_str.replace("ö", "o")
    new_str = new_str.replace("ó", "o")
    new_str = new_str.replace("&", "and")
    new_str = new_str.replace("'", "")
    if new_str.lower() in site_artist_list:
        new_artist_list[item] = "+    " + new_artist_list[item]
        found_artist = found_artist + 1
    if re.search('^The\s', new_str):
        new_str = new_str.replace("The ", "", 1)
        if new_str.lower() in site_artist_list:
            new_artist_list[item] = "+    " + new_artist_list[item]
            found_artist = found_artist + 1
    if re.search('HIM', new_str):
        new_str = new_str.replace("HIM", "H.I.M.")
        if new_str.lower() in site_artist_list:
            new_artist_list[item] = "+    " + new_artist_list[item]
            found_artist = found_artist + 1
    if re.search('Dj Shah', new_str):
        new_str = new_str.replace("Dj Shah", "Roger Shah")
        if new_str.lower() in site_artist_list:
            new_artist_list[item] = "+    " + new_artist_list[item]
            found_artist = found_artist + 1

print("Всего файлов: %d" % len(album_list_files))
print("Всего артистов: %d" % len(new_artist_list))
print("Всего артистов на сайте: %d" % len(site_artist_list))
print("Совпадений: %d" % found_artist)

#   Записываем список в файл
out_file = open(out_folder + "Artist List " + now_time.strftime("%d.%m.%Y") + ".txt", "w", encoding="utf-8")
for item in new_artist_list:
    out_file.write(item)
out_file.close()

input("\n\nНажмите Enter чтобы выйти .")