import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import *
import time
import datetime
from time import sleep
import os

BASE_URL="http://sms-grep-ws.vps126.mtu.immo/actions.php"
DELAY_BETWEEN_RQ = 4
value_days_ago=1
value_days_to=1
#функция по определению даты от которой начинаем отчет
def from_date(value_days_ago):
    value_from_date=datetime.datetime.now() - datetime.timedelta(days=value_days_ago)
    value_from_date=value_from_date.strftime('%d.%m.%Y')
    return value_from_date
#функция по определению вчерашней даты
def yesterday():
    yesterday=datetime.datetime.now() - datetime.timedelta(days=value_days_to)
    yesterday=yesterday.strftime('%d.%m.%Y')
    return yesterday

# (если ежедневный, но за выходные - пт, суб, вчера, т.е. сегодня-3)


#проверка наличия записи report_id

def record_check():
    print('Проверяю готовность отчетов..')
    #sleep(DELAY_BETWEEN_RQ)
    while True:
        r=requests.get(BASE_URL, params={
            'action':'load'
        })
        soup=BeautifulSoup(r.text,'lxml')
        #all_checks=soup.find_all("span", {"class":"text-success"})
        all_checks=soup.find_all('span')
        amount=len(all_checks)
        print(f'Всего {amount} элементов span на странице')
        print(f'Состояние первого: {all_checks[1]}')

        if "Выполнено" not in all_checks[1].text:
            print(f'Есть невыполненный отчет, в элементе span: --{all_checks[1].text} --. Перехожу в ожидание...')
            sleep(DELAY_BETWEEN_RQ)
        else:                
            print('Все задания выполнены, можем скачивать отчет!')
        #print(all_checks)
            return    



#сохранение файла
def download_file(report_id,directory):
    record_check()
    response=requests.get(BASE_URL,params={
     'action': 'get',
     'id': report_id,      
    })
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    if response.status_code == 200:
        with open(f'{directory}/file_{report_id}.zip', 'wb') as f:
            f.write(response.content)
        print('File downloaded \n')
    else:
         print('Unsuccessfull, статус код:', response.status_code) 

# 4312, 4313, 3003(убрали) ID оператора – 520 
def life_rb():
    print('Запрос отчета по Лайф РБ, 4312, 4313')
    requests.get(BASE_URL,params={
       'action': 'add',
        'ops': '520',
        'srcs': '4312, 4313',
        'from': from_date(value_days_ago),
        'to': yesterday()
    })
    print('DONE')
    #переходим на страницу load, чтобы увидеть последние задания на скачивание
    load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

    #загружаем в Суп текст страницы
    soup=BeautifulSoup(load_response.text, 'lxml')
    #ищем все div элементы
    div_elements=soup.find_all('div')
    report_id_found=div_elements[0].text
    #печатаем первый среди div'ов
    print('Номер отчета: '+report_id_found)
    
    download_file(report_id_found, directory='08 - Статистика Life РБ 4312 4313')


# 40449, ID оператора – 79
def short_40449():
    print('Запрос отчета по 40449')
    requests.get(BASE_URL,params={
       'action': 'add',
        'ops': '79',
        'srcs': '40449',
        'from': from_date(value_days_ago),
        'to': yesterday()
    })
    print('DONE')
    #переходим на страницу load, чтобы увидеть последние задания на скачивание
    load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

    #загружаем в Суп текст страницы
    soup=BeautifulSoup(load_response.text, 'lxml')
    #ищем все div элементы
    div_elements=soup.find_all('div')
    report_id_found=div_elements[0].text
    print(report_id_found)
    #печатаем первый среди div'ов
    #sleep(DELAY_BETWEEN_RQ)
    # print(div_elements[0].text)
    download_file(report_id_found, directory='02 - Статистика 40449')

# 4058, ID оператора – 79
def short_4058():
    print('Запрос отчета по 4058')
    requests.get(BASE_URL,params={
        'action': 'add',
        'ops': '79',
        'srcs': '4058',
        'from': from_date(value_days_ago),
        'to': yesterday()
    })
    print('DONE')
    #переходим на страницу load, чтобы увидеть последние задания на скачивание
    load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

    #загружаем в Суп текст страницы
    soup=BeautifulSoup(load_response.text, 'lxml')

    #ищем все div элементы
    div_elements=soup.find_all('div')
    report_id_found=div_elements[0].text
    print(report_id_found)
    #печатаем первый среди div'ов
    #sleep(DELAY_BETWEEN_RQ)
    # print(div_elements[0].text)
    download_file(report_id_found, directory='03 - Статистика 4058')

# 233, 234, 346, 656, 850 (+новые номера с 2025года: 2348
# 2347, 2346) ID оператора – 161
#http://sms-grep-ws.vps126.mtu.immo/actions.php?action=add&ops=161&srcs=233%2C+234%2C+346%2C+656%2C+850&tels=&target=all&from=31.03.2024&to=31.03.2024
def ums():
     print('Запрос отчета по UMS')
     requests.get(BASE_URL,params={
        'action': 'add',
        'ops': '161',
        'srcs': '233, 234, 346, 656, 850, 2348, 2347, 2346',
        'from': from_date(value_days_ago),
        'to': yesterday()
     })
     print('DONE')
     #переходим на страницу load, чтобы увидеть последние задания на скачивание
     load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

     #загружаем в Суп текст страницы
     soup=BeautifulSoup(load_response.text, 'lxml')

     #ищем все div элементы
     div_elements=soup.find_all('div')
     report_id_found=div_elements[0].text
     print(report_id_found)
     #печатаем первый среди div'ов
     #sleep(DELAY_BETWEEN_RQ)
     # print(div_elements[0].text)
     download_file(report_id_found, directory='04 - Статистика UMS')

# Узмобайл 4651, 4652, 3642, 3645, 3646, 3648, 3647 ID оператора – 699
def uzmobile():
    print('Запрос отчета по Uzmobile')
    requests.get(BASE_URL,params={
        'action': 'add',
        'ops': '699',
        'srcs': '4651, 4652, 3642, 3645, 3646, 3648, 3647',
        'from': from_date(value_days_ago),
        'to': yesterday()
    })
    print('DONE')
    #переходим на страницу load, чтобы увидеть последние задания на скачивание
    load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

    #загружаем в Суп текст страницы
    soup=BeautifulSoup(load_response.text, 'lxml')

    #ищем все div элементы
    div_elements=soup.find_all('div')
    report_id_found=div_elements[0].text
    print(report_id_found)
    #печатаем первый среди div'ов
    #sleep(DELAY_BETWEEN_RQ)
    # print(div_elements[0].text)
    download_file(report_id_found, directory='05 - Статистика Узмобайл')

# 40453, 40456 ID оператора – 79
def short_40453_40456():
    print('Запрос отчета по 40453 40456')
    requests.get(BASE_URL,params={
        'action': 'add',
        'ops': '79',
        'srcs': '40453, 40456',
        'from': from_date(value_days_ago),
        'to': yesterday()
    })
    print('DONE')
    #переходим на страницу load, чтобы увидеть последние задания на скачивание
    load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

    #загружаем в Суп текст страницы
    soup=BeautifulSoup(load_response.text, 'lxml')

    #ищем все div элементы
    div_elements=soup.find_all('div')
    report_id_found=div_elements[0].text
    print(report_id_found)
    #печатаем первый среди div'ов
    #sleep(DELAY_BETWEEN_RQ)
    # print(div_elements[0].text)
    download_file(report_id_found, directory='09 - Статистика 40453 40456')

# Доп функция 363131, 362121, 361212, 363132  оператор 52 МТС РБ
def short_mts_rb():
    print('Запрос отчета по 363131, 362121, 361212, 363132  оператор МТС РБ')
    requests.get(BASE_URL,params={
        'action': 'add',
        'ops': '52',
        'srcs': '363131, 362121, 361212, 363132',
        'from': from_date(value_days_ago),
        'to': yesterday()
    })
    print('DONE')
    #переходим на страницу load, чтобы увидеть последние задания на скачивание
    load_response=requests.get('http://sms-grep-ws.vps126.mtu.immo/actions.php?action=load')

    #загружаем в Суп текст страницы
    soup=BeautifulSoup(load_response.text, 'lxml')

    #ищем все div элементы
    div_elements=soup.find_all('div')
    report_id_found=div_elements[0].text
    print(report_id_found)
    #печатаем первый среди div'ов
    #sleep(DELAY_BETWEEN_RQ)
    # print(div_elements[0].text)
    download_file(report_id_found, directory='01 - Стата МТС - weekly')

#Функция получения количества дней назад
def get_days_ago():
    global value_days_ago
    value_days_ago = int(entry1.get())
    print(f'Расчитываем от {value_days_ago} дней назад')

    #Функция получения количества дней end date
def get_days_to():
    global value_days_to
    value_days_to= int(entry3.get())
    print(f'Расчитываем по {value_days_to} дней назад')
    



root=tk.Tk()
root.title("Отчеты из Grep")
root.geometry("250x350")

button1=tk.Button(root, text="40449", command=short_40449)
button2=tk.Button(root, text="4058", command=short_4058)
button3=tk.Button(root, text="UMS", command=ums)
button4=tk.Button(root, text="Uzmobile", command=uzmobile)
button5=tk.Button(root, text="40453_40456", command=short_40453_40456)
button6=tk.Button(root, text="Life_RB", command=life_rb)
button7=tk.Button(root, text="MTS_РБ - weekly", command=short_mts_rb)

button1.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()
button6.pack()
button7.pack()
#поле и кнопка для приема начальной даты - старая кнопка
#entry1=Entry(root, width=5)
#entry1.pack()
#button8=Button(root, text="дней назад (1 by default)", pady=10, command=get_days_ago)
#button8.pack()

#поле и кнопка для приема начальной даты
entry1=Entry(root, width=5)
entry1.pack()
button9=Button(root, text="начиная с:", pady=10, command=get_days_ago)
button9.pack()

#поле и кнопка для приема конечной даты
entry3=Entry(root, width=5)
entry3.pack()
button10=Button(root, text="оканчивая:", pady=10, command=get_days_to)
button10.pack()



#проверяем доступ к Грепу (вне функций)
grep_response=requests.get("http://sms-grep-ws.vps126.mtu.immo/")
print(grep_response.status_code)
#data_file=requests.get("http://sms-grep-ws.vps126.mtu.immo/actions.php?action=add&ops=79&srcs=40449&tels=&target=all&from=27.03.2024&to=27.03.2024")


from_date(value_days_ago)
print(f'Расчитываем от {value_days_ago} дней назад')


root.mainloop()








