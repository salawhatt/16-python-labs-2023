from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
import matplotlib.pyplot as plt


URL = 'https://ruz.spbstu.ru'                            # будет дополнен параметрами
URL_search = 'https://ruz.spbstu.ru/search/groups?q=48'  # поисковая строка
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}                                                       # пробрасываемые заголовки (симуляция действий реального человека)


def get_group_number():
    group_number = input('Введите номер группы (*******/*****): ')
    return group_number


def find_group_number(num_group):
    global URL
    html = requests_html(URL_search)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='groups-list__item')
    groups = []
    count_gr = 0
    for group in items:
        groups.append(
            {
                0: group.find('a', class_='groups-list__link').get_text(),
                1: group.find('a', class_='groups-list__link').get('href')
            }
        )
        count_gr += 1
    for i in range(count_gr):
        if groups[i][0] == num_group:
            URL = URL + groups[i][1]
            return 1
    print("Номер группы не найден")
    exit(0)


# запрос на страницу, забираем HTML c пробросом заголовков
def requests_html(URL):
    return requests.get(URL, headers=HEADERS).text

# определить чётность недели
def determine_week(soup):
    items = soup.find('h3', class_='page__h3').text
    if r'нечётная' in items:
        return 'нечётная неделя'
    else:
        return 'чётная неделя'


def get_data():
    html = requests_html(URL)
    soup = BeautifulSoup(html, 'html.parser')   # получение объекта страницы. пробрасываем html и обращаемся к парсеру
    week = determine_week(soup)
    items = soup.find_all('li', class_='schedule__day')  # считываем блоки содержащие дни с лекциями
    print('\n------------------------------------\n Расписание (', week, ')')
    dates_set = []  # массив для дней в которые есть пары
    for date in items:
        dates_set.append(
            {
                0: date.find('div', class_='schedule__date').get_text()
            }
        )
    types_names = ['', 'Тип пары:', 'Место проведения:', 'Преподаватель:']
    count_dat = [0] * 7  # массив для подсчёта количества пар в днях
    index = [0]*len(items)  # массив для индексов дня в которые есть пары
    tmp = 0  # временный индекс для index
    # цикл по всем блокам с днями
    for less_num in range(len(items)):
        print('\t \n Дата проведения:', dates_set[less_num][0])
        less_info = []  # массив для информации о парах в одном дне
        lessons = items[less_num].find_all('li', class_='lesson')  # считывание блоков содержащих пары в одном дне
        count_lessons = 0  # счётчик пар
        # запись данных о парах в множество
        for lesson in lessons:
            less_info.append(
                {
                 0: lesson.find('div', class_='lesson__subject').get_text(),
                 1: lesson.find('div', class_='lesson__type').get_text(),
                 2: lesson.find('div', class_='lesson__places').get_text()
                }
                 )
            # не всегда указан преподаватель, поэтому нужно использовать исключение try
            try:
                less_info[count_lessons].update({3: lesson.find('div', class_='lesson__teachers').get_text()})
            except AttributeError:
                less_info[count_lessons].update({3: "Не опредлено"})
            count_lessons += 1

        days_on_week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вск']
        # если в день недели есть пара, то сохраняем индекс дня недели
        for num in range(len(days_on_week)):
            if days_on_week[num] in dates_set[less_num][0]:
                index[tmp] = num
                tmp += 1
        # вывод пар в одном дне
        for cur_less in range(count_lessons):
            print('---------', cur_less+1, '------------------------')
            # подсчёт количества пар в дне
            count_dat[index[less_num]] += 1
            for data_type in range(4):
                print(types_names[data_type], less_info[cur_less][data_type])
    return count_dat


def get_date_day():
    global URL
    months = ['янв', 'февр', 'мар', 'апр', 'май', 'июнь', 'июль', 'авг', 'сент', 'окт', 'ноя', 'дек']
    date = input('Введите дату (дд.мм.гггг): ')
    try:
        valid_date = time.strptime(date, '%d.%m.%Y')
    except ValueError:
        print('Неверная дата!')
        exit(0)
    if date[6:10] != '2023':
        print('Неверный год!')
        exit(0)
    URL = URL+'?date=2023-' + date[3:5] + '-' + date[0:2]


def main():
    find_group_number(get_group_number())
    get_date_day()
    count_dat = get_data()
    plt.plot(['пн', 'вт', 'ср', 'чт', 'пт', 'cуб', 'вск'], count_dat)
    plt.show()


main()