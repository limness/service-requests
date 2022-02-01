
from decimal import *
from linear_analysis import Stats
from collections import Counter

from kucoin_config import client
from datetime import datetime
from math import sqrt


##################
def get_extremes(price_list):

    extremes = []
    time = 0
    now_min = True

    for index, price in enumerate(price_list):
        if index + 1 < len(price_list):
            time += 1
            # Если сейчас мы в точке минимума
            if now_min:
                # Если следующая точка больше, значит мы в точке минимума
                if price_list[index + 1] > price:
                    # [Индекс] [Цена] [Падение/Рост] [Время в минутах]
                    extremes.append([index, price, 0, time])
                    now_min = False
                    time = 0
            # Если сейчас мы в точке максимума
            else:
                # Если следующая точка меньше, значит мы в точке максмиму
                if price_list[index + 1] < price: #[1]
                    # [Индекс] [Цена] [Падение/Рост] [Время в минутах]
                    extremes.append([index, price, 1, time])
                    now_min = True
                    time = 0

    return extremes

def get_percent_extremes(percent, price_list):

    extremes = []
    #time = 0
    #now_min = True
    now_point = 0

    # maximum = 0
    # minimum = 0

    for index, price in enumerate(price_list):
        if index == 0:
            now_point = price
            # [Индекс] [Цена] [Падение/Рост] [Время в минутах]
            extremes.append([index, price, 1, 0])
        else:
            # Если N-ая цена в графике больше на X% последней точки
            if price > now_point + now_point / 100 * percent:
                now_point = price
                # [Индекс] [Цена] [Падение/Рост/Холд] [Время в минутах]
                extremes.append([index, price, 1, 0])
            # Если N-ая цена в графике меньше на X%  последней точки
            elif price < now_point - now_point / 100 * percent:
                now_point = price
                # [Индекс] [Цена] [Падение/Рост/Холд] [Время в минутах]
                extremes.append([index, price, 0, 0])
            else:
                # maximum = max(maximum, price)
                # minimum = max(maximum, price)
                # [Индекс] [Цена] [Падение/Рост/Холд] [Время в минутах]
                extremes.append([index, price, 2, 0])

    # Инфа по тренду
    # 0 - в экстремуме падения
    # 1 - в экстремуме роста
    # 2 - процесс падения
    # 3 - процесс роста
    #trend_info = 0

    # Поворачиваем массив
    # И там где идет экстремум роста/падения - проходим по всем процессам холда и устанавливаем соотв. индикатор
    # for index, extreme in enumerate(reversed(extremes)):
    #     #print(extreme[2], end='')
    #     # Если мы в экстремуме падения
    #     if extreme[2] == 0:
    #         trend_info = 2
    #     # Если мы в экстремуме роста
    #     elif extreme[2] == 1:
    #         trend_info = 3
    #     # Если мы в процессе холда
    #     else:
    #         extreme[2] = trend_info
            #print(f'sueta {trend_info}')
        # Если мы в процессе холда
        # elif extreme[2] == 2:
        #     # Если холдимся перед экстремумом падения - значит тренд нисходящий
        #     if trend_info == 0:
        #         # 2 - процесс падения
        #         extremes[index][2] = 2
        #     # Если холдимся перед экстремумом роста - значит тренд восходящий
        #     elif trend_info == 1:
        #         # 2 - процесс роста
        #         extremes[index][2] = 3

    # for extreme in extremes:
    #     print(extreme[2], end='')
    # for index, price in enumerate(price_list):
    #     if index + 1 < len(price_list):
    #         time += 1
    #         # Если сейчас мы в точке минимума
    #         if now_min:
    #             # Если следующая точка больше на N%, значит мы в точке минимума
    #             if price_list[index + 1] > price:
    #                 # [Индекс] [Цена] [Падение/Рост] [Время в минутах]
    #                 extremes.append([index, price, 0, time])
    #                 now_min = False
    #                 time = 0
    #         # Если сейчас мы в точке максимума
    #         else:
    #             # Если следующая точка меньше, значит мы в точке максмиму
    #             if price_list[index + 1] < price:
    #                 # [Индекс] [Цена] [Падение/Рост] [Время в минутах]
    #                 extremes.append([index, price, 1, time])
    #                 now_min = True
    #                 time = 0
    return extremes


def get_pair_daily_stat(pair):
    # Подсчет времени для статистики
    before = datetime.now()

    # Данные для построения графика изменения цен
    #graphic = []

    # Данные экстремума
    #graphic_sorted = []

    with open(f'pairs-klines/{pair}.txt', 'r') as reader:
        lines = reader.readlines()

    # Читаем из файла все изменения цены
    price_list = [float(pair.split(' ')[1].strip()) for pair in reversed(lines)]

    #print(f"Now: {price_list[0]}")

    # for index, price in enumerate(price_list):
    #     graphic.append([index, price, 'NOTHING'])

    ###########################
    # Точки экстремума графика
    extremes = get_extremes(price_list)

    total_length = 0
    total_count = 0

    length_list = []

    ###########################
    # Получаем длины всех изменений тренда за сутки
    ###########################

    for index, extreme in enumerate(extremes):
        if index == 0:
            continue

        length = sqrt((extremes[index][1] - extremes[index - 1][1]) ** 2)
        procent_change = extremes[index][1] / (extremes[index - 1][1] / 100) - 100
        time = extremes[index][3]

        if index % 2 == 0:
            length_list.append([-length, procent_change, time])
        else:
            length_list.append([length, procent_change, time])

    ###########################

    total_profit = 0
    total_profit_precent = 0
    total_profit_count = 0
    total_profit_time = 0

    total_lose = 0
    total_lose_precent = 0
    total_lose_count = 0
    total_lose_time = 0

    total_length = []

    for index, item in enumerate(length_list):
        total_length.append(item[1])
        #print(f"Размер изменения: {item[0]} ({item[1]}%) ({item[2]} м.)")
        if item[0] > 0:
            total_profit += item[0]
            total_profit_precent += item[1]
            total_profit_count += 1
            total_profit_time += item[2]
        else:
            total_lose += item[0]
            total_lose_precent += item[1]
            total_lose_count += 1
            total_lose_time += item[2]

        #graphic_sorted.append([index, item, 'NOTHING'])

    after = datetime.now()

    daily_info = {
        'LiftsCount' : total_profit_count,
        'FallsCount' : total_lose_count,
        'MaxLift' : round(max(total_length), 4),
        'MaxFall' : round(min(total_length), 4),
        'LiftsAverageTime' : round(total_profit_time / total_profit_count, 2),
        'FallsAverageTime' : round(total_lose_time / total_lose_count, 2),
        'LiftsAverageProcent' : round(total_profit_precent / total_profit_count, 4),
        'FallsAverageProcent' : round(total_lose_precent / total_lose_count, 4),
    }
    return daily_info


def get_buy_extremes(percent, price_list):

    extremes = {}

    now_point = 0

    best_buy = {
        'Index' : 0,
        'Price' : 9999999,
    }
    best_sell = {
        'Index' : 0,
        'Price' : -9999999,
    }
    # maximum = 0
    # minimum = 90000

    for index, price in enumerate(price_list):
        if index == 0:
            now_point = price

        if best_buy['Price'] > price:
            best_buy['Index'] = index
            best_buy['Price'] = price

        if best_sell['Price'] < price:
            best_sell['Index'] = index
            best_sell['Price'] = price
            # [Индекс] [Цена] [Падение/Рост] [Время в минутах]
            #extremes.append([index, price, 1, 0])
        #else:
        # Если N-ая цена в графике больше на X% последней точки
        if price > now_point + now_point / 100 * percent:
            now_point = price
            extremes[best_buy['Index']] = {'Buy' : True, 'Sell' : False}
            best_buy['Index'] = 0
            best_buy['Price'] = 9999999

        #    print('sueta')
        # Если N-ая цена в графике меньше на X%  последней точки
        # elif price < now_point - now_point / 100 * percent:
        #     now_point = price
            # [Индекс] [Цена] [Падение/Рост/Холд] [Время в минутах]
            #extremes.append([index, price, 1, 0])
        # Если N-ая цена в графике меньше на X%  последней точки
        elif price < now_point - now_point / 100 * percent:
            now_point = price
            extremes[best_sell['Index']] = {'Buy' : False, 'Sell' : True}
            best_sell['Index'] = 0
            best_sell['Price'] = -9999999
            # [Индекс] [Цена] [Падение/Рост/Холд] [Время в минутах]
            #extremes.append([index, price, 0, 0])
    #    else:

            # if best_sell['Price'] < price:
            #     #maximum = price
            #     best_sell['Index'] = index
            #     best_sell['Price'] = price
            # [Индекс] [Цена] [Падение/Рост/Холд] [Время в минутах]
            #extremes.append([index, price, 2, 0])

    return extremes

def get_extremes_to_buy(lines, pair):
    # Данные для построения графика изменения цен
    graphic = []

    # Читаем из файла все изменения цены
    price_list = [candle[0] for candle in lines]

    #print(f"Now: {price_list[0]}")

    # for index, price in enumerate(price_list):
    #     graphic.append([index, price, 'NOTHING'])

    ###########################
    # Точки экстремума графика

    #print(price_list)
    extremes = get_buy_extremes(Decimal("0.8"), price_list)#get_extremes(price_list)
    #extremes = get_percent_extremes()#get_buy_extremes(price_list)

    #print(extremes)
    # for index, price in enumerate(price_list):
    #     graphic.append([index, price, 'NOTHING'])
    #
    #     if index in extremes and extremes[index]['Sell']:
    #         graphic.append([index, price, 'SELL'])
    #     elif index in extremes and extremes[index]['Buy']:
    #         graphic.append([index, price, 'BUY'])
    # #
    # stats = Stats()
    # stats.BuildStat(graphic, []) #last_deltas

    return extremes


def get_pair_daily_procents(pair):

    # Все изменения цены
    price_list = []

    # Пытаемся загрузить данные из файла
    try:
        with open(f'pairs-klines/{pair}.txt', 'r') as reader:
            lines = reader.readlines()

        # Читаем из файла все изменения цены
        price_list = [float(pair.split(' ')[1].strip()) for pair in reversed(lines)]

    # Файла нет, придется взять данные с биржи
    except FileNotFoundError:
        date_begin = int(datetime.now().timestamp() - 60 * 60 * 24)
        date_end = int(datetime.now().timestamp())

        klines = client.get_kline_data(pair, '1min', date_begin, date_end)

        # Читаем из запроса все изменения цены
        price_list = [float(kline[1]) for kline in klines]

    ###########################
    # Точки графика
    extremes = price_list

    total_length = 0
    total_count = 0

    length_list = []

    ###########################
    # Получаем длины всех изменений тренда за сутки
    ###########################
    procent_list_minus = []
    procent_list_plus = []
    procent_list_modules = []

    for index, extreme in enumerate(extremes):
        if index == 0:
            continue

        procent_change = extremes[index] / (extremes[index - 1] / 100) - 100

        if procent_change > 0:
            procent_list_plus.append(procent_change)
            procent_list_modules.append(procent_change)
        else:
            procent_list_minus.append(procent_change)
            procent_list_modules.append(-procent_change)

    ###########################

    daily_procents = {
        'ProcentsPlus' : procent_list_plus,
        'ProcentsMinus' : procent_list_minus,
        'ProcentsModules' : procent_list_modules
    }
    return daily_procents

    # print()
    # print(after - before)
    # print()
    # print(f"Число подъемов: {total_profit_count} ### Среднее время: {round(total_profit_time / total_profit_count, 2)} м. ### Средний размер подъемов за сутки: {round(total_profit / total_profit_count, 4) * 2} ({round(total_profit_precent / total_profit_count, 4) * 2}%)")
    # print(f"Число падений: {total_lose_count} ### Среднее время: {round(total_lose_time / total_lose_count, 2)} м. ### Средний размер падений за сутки: {round(total_lose / total_lose_count, 4) * 2} ({round(total_lose_precent / total_lose_count, 4) * 2}%)")
    #
    # # Объявляем конструктор для класса сбора статистики и подсчета тренда
    # stats = Stats()
    # stats.BuildStat(graphic, []) #last_deltas
    # stats.BuildStat(graphic_sorted, []) #last_deltas
    # stats.BuildCorrelation(graphic_sorted)

def get_graphic_test(pair, percent=Decimal("0.8")):
    # Подсчет времени для статистики
    before = datetime.now()

    # Данные для построения графика изменения цен
    #graphic = []

    # Данные экстремума
    graphic_sorted = []

    with open(f'pairs-klines/{pair}.txt', 'r') as reader:
        lines = reader.readlines()

    # Читаем из файла все изменения цены
    price_list = [Decimal(pair.split(' ')[1].strip()) for pair in reversed(lines)]

    #print(f"Now: {price_list[0]}")

    # for index, price in enumerate(price_list):
    #     graphic.append([index, price, 'NOTHING'])

    ###########################
    # Точки экстремума графика
    extremes = get_percent_extremes(percent, price_list)

    total_length = 0
    total_count = 0

    length_list = []

    #for index, extreme in enumerate(extremes):
    #    graphic_sorted.append([index, Decimal(f"{extreme[1]}"), 'NOTHING'])


    ###########################
    # Получаем длины всех изменений тренда за сутки
    ###########################

    # Линии падения и подъема (полные)
    total_lines = []
    now_min = False

    for index, extreme in enumerate(extremes):

        #graphic_sorted.append([index, Decimal(extreme[1]), 'NOTHING'])

        if index == 0:
            total_lines.append(0)
            continue

        if now_min:
        #if False:
            # График продолжает движение вниз
            if extremes[index-1][1] > extremes[index][1]:
                # Отнимаем от изначальной точки в начале падения 0.8 процентов
                total_lines[-1] -= 1
            # График изменил движение
            if extremes[index-1][1] < extremes[index][1]:
                now_min = False
                total_lines.append(0)
                total_lines[-1] += 1

        else:
            # График продолжает движение вверх
            if extremes[index-1][1] < extremes[index][1]:
                # Прибавляем к изначальной точки в начале подъема 0.8 процентов
                total_lines[-1] += 1
            # График изменил движение
            if extremes[index-1][1] > extremes[index][1]:
                #break
                now_min = True
                total_lines.append(0)
                total_lines[-1] -= 1

        # length = sqrt((extremes[index][1] - extremes[index - 1][1]) ** 2)
        # procent_change = extremes[index][1] / (extremes[index - 1][1] / 100) - 100
        # time = extremes[index][3]
        #
        # if index % 2 == 0:
        #     length_list.append([-length, procent_change, time])
        # else:
        #     length_list.append([length, procent_change, time])

    sorted_lines = []
    for index, line in enumerate(total_lines):
        if Decimal(line) < 0:
            sorted_lines.append(Decimal(line))
            #print(Decimal(line))
        graphic_sorted.append([index, Decimal(line), 'NOTHING'])


    coin_counter = Counter(sorted_lines)

    #print(coin_counter)

    optimal_percent = 0

    for weight in coin_counter.most_common():
        optimal_percent += (weight[0] * Decimal("0.8")) * weight[1]
        #print(f"{weight[0]} * {weight[1]} = {(weight[0] * 0.8) * weight[1]}")

    optimal_percent = optimal_percent / sum([num[1] for num in coin_counter.most_common()])
    #optimal_percent = round(optimal_percent, 2)
    #print(total_weight)

    ###########################
    # Получаем длины всех изменений тренда за сутки
    ###########################

    for index, extreme in enumerate(extremes):
        if index == 0:
            continue

        length = sqrt((extremes[index][1] - extremes[index - 1][1]) ** 2)
        procent_change = extremes[index][1] / (extremes[index - 1][1] / 100) - 100
        time = extremes[index][3]

        if index % 2 == 0:
            length_list.append([-length, procent_change, time])
        else:
            length_list.append([length, procent_change, time])

    ###########################

    total_profit = 0
    total_profit_precent = 0
    total_profit_count = 0
    total_profit_time = 0

    total_lose = 0
    total_lose_precent = 0
    total_lose_count = 0
    total_lose_time = 0

    total_length = []

    for index, item in enumerate(length_list):
        total_length.append(item[1])
        if item[0] > 0:
            total_profit += item[0]
            total_profit_precent += item[1]
            total_profit_count += 1
            total_profit_time += item[2]
        else:
            total_lose += item[0]
            total_lose_precent += item[1]
            total_lose_count += 1
            total_lose_time += item[2]

        #graphic_sorted.append([index, item, 'NOTHING'])

    after = datetime.now()

    daily_info = {
        'LiftsCount' : total_profit_count,
        'FallsCount' : total_lose_count,
        'MaxLift' : round(max(total_length), 4),
        'MaxFall' : round(min(total_length), 4),
        'LiftsAverageTime' : round(total_profit_time / total_profit_count, 2),
        'FallsAverageTime' : round(total_lose_time / total_lose_count, 2),
        'LiftsAverageProcent' : round(total_profit_precent / total_profit_count, 4),
        'FallsAverageProcent' : round(total_lose_precent / total_lose_count, 4),
        'FallsSueta' : round(total_lose_precent / total_lose_count / 1, 4),
        'FallsOptimal' : Decimal(f"{optimal_percent}"),
    }

    #print(graphic_sorted)
    ###########################
    # Получаем длины всех изменений тренда за сутки
    ###########################

    # for index, extreme in enumerate(extremes):
    #     if index == 0:
    #         continue
    #
    #     length = sqrt((extremes[index][1] - extremes[index - 1][1]) ** 2)
    #     procent_change = extremes[index][1] / (extremes[index - 1][1] / 100) - 100
    #     time = extremes[index][3]
    #
    #     if index % 2 == 0:
    #         length_list.append([-length, procent_change, time])
    #     else:
    #         length_list.append([length, procent_change, time])

    ###########################

    # total_profit = 0
    # total_profit_precent = 0
    # total_profit_count = 0
    # total_profit_time = 0
    #
    # total_lose = 0
    # total_lose_precent = 0
    # total_lose_count = 0
    # total_lose_time = 0
    #
    # total_length = []

    # for index, item in enumerate(length_list):
    #     total_length.append(item[1])
    #     #print(f"Размер изменения: {item[0]} ({item[1]}%) ({item[2]} м.)")
    #     if item[0] > 0:
    #         total_profit += item[0]
    #         total_profit_precent += item[1]
    #         total_profit_count += 1
    #         total_profit_time += item[2]
    #     else:
    #         total_lose += item[0]
    #         total_lose_precent += item[1]
    #         total_lose_count += 1
    #         total_lose_time += item[2]
    #
    #     graphic_sorted.append([index, item, 'NOTHING'])

    #stats = Stats()
    #stats.BuildStat(graphic_sorted, []) #last_deltas

    #after = datetime.now()

    # daily_info = {
    #     'LiftsCount' : total_profit_count,
    #     'FallsCount' : total_lose_count,
    #     'MaxLift' : round(max(total_length), 4),
    #     'MaxFall' : round(min(total_length), 4),
    #     'LiftsAverageTime' : round(total_profit_time / total_profit_count, 2),
    #     'FallsAverageTime' : round(total_lose_time / total_lose_count, 2),
    #     'LiftsAverageProcent' : round(total_profit_precent / total_profit_count, 4),
    #     'FallsAverageProcent' : round(total_lose_precent / total_lose_count, 4),
    # }
    return daily_info


def get_heiken_candles(candles):
    candles_heiken = []

    for index, candle in enumerate(candles):
        #print(f"need {candles[index]}")
        #print(candles[index]['Open'])
        candle_open = candles[index]['Open']
        candle_close = candles[index]['Close']

        if index > 0:
            #print(candles_heiken)

            candle_open = (candles_heiken[index-1]['Open'] + candles_heiken[index-1]['Close']) / 2
            candle_close = (candles[index]['Open'] + candles[index]['Close'] + candles[index]['High'] + candles[index]['Low']) / 4
        # else:
        #     # Добавим первую свечу, чтобы в дальнейшем работать на ее основе
        #     candles_heiken.append(candles[0])

        # candles_heiken[index]['Time'] = candles[index]['Time']
        # candles_heiken[index]['High'] = candles[index]['High']
        # candles_heiken[index]['Low'] = candles[index]['Low']

        candle_info = {
            'Time' : candles[index]['Time'],
            'Open' : candle_open,
            'Close' : candle_close,
            'High' : candles[index]['High'],
            'Low' : candles[index]['Low'],
        }
        candles_heiken.append(candle_info)

        # if index > 0:
        #     c_open = (candles[index-1]['Open'] + candles[index-1]['Close']) / 2
        #     c_close = (candles[index]['Open'] + candles[index]['Close'] + candles[index]['High'] + candles[index]['Low']) / 4
        # else:
        #     c_open = candles[index]['Open']
        #     c_close = candles[index]['Close']
        #
        # candle_info = {
        #     'Time' : candles[index]['Time'],
        #     'Open' : c_open,
        #     'Close' : c_close,
        #     'High' : candles[index]['High'],
        #     'Low' : candles[index]['Low'],
        # }
        #candles_heiken.append(candle_info)

    return candles_heiken

def get_heiken_candles_sueta(candles):
    candles_heiken = []

    for index, candle in enumerate(candles):
        candle_open = candles[index][0]
        candle_close = candles[index][1]

        if index > 0:
            candle_open = (candles_heiken[index-1][0] + candles_heiken[index-1][1]) / 2
            candle_close = (candles[index][0] + candles[index][1] + candles[index][2] + candles[index][3]) / 4
        # else:
        #     c_open = candles[index][0]
        #     c_close = candles[index][1]

        # c_high = candles[index][2]
        # c_low = candles[index][3]
        #
        # candles_heiken.append([c_open, c_close, c_high, c_low])
        candle_info = [
            candle_open,
            candle_close,
            candles[index][2],
            candles[index][3],
        ]
        candles_heiken.append(candle_info)

    return candles_heiken

# def get_heiken_candles_sueta(candles):
#     candles_heiken = []
#
#     for index, candle in enumerate(candles):
#
#         if index > 0:
#             c_open = (candles[index-1][0] + candles[index-1][1]) / 2
#             c_close = (candles[index][0] + candles[index][1] + candles[index][2] + candles[index][3]) / 4
#         else:
#             c_open = candles[index][0]
#             c_close = candles[index][1]
#
#         c_high = candles[index][2]
#         c_low = candles[index][3]
#
#         candles_heiken.append([c_open, c_close, c_high, c_low])
#
#     return candles_heiken

def get_heiken_graphic(pair):
    # Подсчет времени для статистики
    before = datetime.now()

    # Данные для построения графика изменения цен
    #graphic = []

    # Данные экстремума
    graphic_sorted = []

    with open(f'pairs-klines/{pair}.txt', 'r') as reader:
        lines = reader.readlines()

    # Читаем из файла все изменения цены
    #price_list = [float(pair.split(' ')[1].strip()) for pair in reversed(lines)]
    candles = [[Decimal(candle) for candle in pair.split(' ')] for pair in reversed(lines)]
    #candles = [float(pair) for pair in candles]

    # Time, Open, Close, High, Low
    # writer.write(f"{kline[0]} {kline[1]} {kline[2]} {kline[3]} {kline[4]}\n")

    #print(candles)

    candles_heiken = get_heiken_candles(candles)

    #print(candles_heiken)
    #print(f"Now: {price_list[0]}")

    for index, candle in enumerate(candles): #candles_heiken
        graphic_sorted.append([index, candle[1], 'NOTHING'])

    # for index, candle in enumerate(candles):
    #     graphic_sorted.append([index, candle[0], 'NOTHING'])

    ###########################
    # Точки экстремума графика
    #extremes = get_percent_extremes(0.4, price_list)

    #total_length = 0
    #total_count = 0

    #length_list = []

    #for index, extreme in enumerate(extremes):
    #    graphic_sorted.append([index, Decimal(f"{extreme[1]}"), 'NOTHING'])

    #print(graphic_sorted)
    ###########################
    # Получаем длины всех изменений тренда за сутки
    ###########################

    # for index, extreme in enumerate(extremes):
    #     if index == 0:
    #         continue
    #
    #     length = sqrt((extremes[index][1] - extremes[index - 1][1]) ** 2)
    #     procent_change = extremes[index][1] / (extremes[index - 1][1] / 100) - 100
    #     time = extremes[index][3]
    #
    #     if index % 2 == 0:
    #         length_list.append([-length, procent_change, time])
    #     else:
    #         length_list.append([length, procent_change, time])

    ###########################

    # total_profit = 0
    # total_profit_precent = 0
    # total_profit_count = 0
    # total_profit_time = 0
    #
    # total_lose = 0
    # total_lose_precent = 0
    # total_lose_count = 0
    # total_lose_time = 0
    #
    # total_length = []

    # for index, item in enumerate(length_list):
    #     total_length.append(item[1])
    #     #print(f"Размер изменения: {item[0]} ({item[1]}%) ({item[2]} м.)")
    #     if item[0] > 0:
    #         total_profit += item[0]
    #         total_profit_precent += item[1]
    #         total_profit_count += 1
    #         total_profit_time += item[2]
    #     else:
    #         total_lose += item[0]
    #         total_lose_precent += item[1]
    #         total_lose_count += 1
    #         total_lose_time += item[2]
    #
    #     graphic_sorted.append([index, item, 'NOTHING'])

    stats = Stats()
    stats.BuildStat(graphic_sorted, []) #last_deltas

    #after = datetime.now()

    # daily_info = {
    #     'LiftsCount' : total_profit_count,
    #     'FallsCount' : total_lose_count,
    #     'MaxLift' : round(max(total_length), 4),
    #     'MaxFall' : round(min(total_length), 4),
    #     'LiftsAverageTime' : round(total_profit_time / total_profit_count, 2),
    #     'FallsAverageTime' : round(total_lose_time / total_lose_count, 2),
    #     'LiftsAverageProcent' : round(total_profit_precent / total_profit_count, 4),
    #     'FallsAverageProcent' : round(total_lose_precent / total_lose_count, 4),
    # }
    #return daily_info


def we_should_average(candles, offset): #we_should_average_sueta
    #print(f"pre {candles[-offset]['Close']}")
    # Если цена закрытия предыдущей свечи меньше текущей
    # Значит график поменял тренд на восходящий, пора усреднять
    if candles[-offset]['Close'] < candles[-2]['Close']:
        return True
    else:
        return False

def we_should_average_sueta(candles, index):

    # Если цена закрытия предыдущей свечи меньше текущей
    # Значит график поменял тренд на восходящий, пора усреднять
    if candles[index-2][2] < candles[index-1][2]:
        return True
    else:
        return False

def we_should_buy(candles, index):

    # Если цена закрытия предыдущей свечи меньше текущей
    # Значит график поменял тренд на восходящий, пора усреднять
    if candles[index-2][2] > candles[index-1][2]:
        return True
    else:
        return False
