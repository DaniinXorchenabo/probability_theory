from collections import Counter
from scipy import stats
import numpy as np

pirson_krit = {1.0: {0.01: 6.6, 0.025: 5.0, 0.05: 3.8, 0.95: 0.0039, 0.975: 0.00098, 0.89: 0.00016},
               2.0: {0.01: 9.2, 0.025: 7.4, 0.05: 6.0, 0.95: 0.103, 0.975: 0.051, 0.89: 0.02},
               3.0: {0.01: 11.3, 0.025: 9.4, 0.05: 7.8, 0.95: 0.352, 0.975: 0.051, 0.89: 0.02},
               4.0: {0.01: 13.3, 0.025: 11.1, 0.05: 9.5, 0.95: 0.711, 0.975: 0.484, 0.89: 0.297},
               5.0: {0.01: 15.1, 0.025: 12.8, 0.05: 11.1, 0.95: 1.15, 0.975: 0.831, 0.89: 0.554},
               6.0: {0.01: 16.8, 0.025: 14.4, 0.05: 12.6, 0.95: 1.64, 0.975: 1.24, 0.89: 0.872},
               7.0: {0.01: 18.5, 0.025: 16.0, 0.05: 14.1, 0.95: 2.17, 0.975: 1.69, 0.89: 1.24}}


def print_arr(arr):
    print(*arr, sep='\n')


def print_as_table(arr: list[list[int, int]]):
    print('Вариационный ряд:')
    print("_" * (len(arr) * 5 + 1))
    [print("|" + '|'.join([str(j).center(4) for j in i]) + '|') for i in zip(*arr)]
    print("¯" * (len(arr) * 5 + 1))


def print_min_max(arr, c=9):
    print("Рамах варьирования:",
          r_ := ((_max := max(arr, key=lambda i: i[0])[0]) - (_min := min(arr, key=lambda i: i[0])[0])))
    print('Шаг', setup := round(r_ / c, 2))
    col = [(round(i * setup + _min, 2), round((i + 1) * setup + _min, 2)) for i in range(c)]
    col[-1] = col[-1][0], _max
    col_str = [f'{i} <= x < {j}' for [i, j] in col]
    col_str[-1] = col_str[-1].replace('< ', '<= ')

    div_arr = dict()
    for [_mi, _ma] in col:
        ind = round((_mi + _ma) / 2, 3)
        for [i, count_] in arr:
            if _mi <= i <= _ma:
                div_arr[ind] = div_arr.get(ind, 0) + count_

    # print(div_arr)
    max_len = len(max(col_str, key=len)) + 2
    print('Интервалы:'.center(max_len) \
          + "|     |       |" + " Гистограмма:" \
          + '\n' + '\n'.join(
        [i.center(max_len) + "| " \
         + str(data[1]).center(4) + "| " \
         + str(data[1] / 100).center(6) + "" \
         + "|" + "■" * data[1]
         for [i, data] in zip(col_str, div_arr.items())]))

    col_str.append(f'x < {_max}')

    _func = [sum(_i[1] for _i in list(div_arr.items())[:ind + 1]) / 100 for ind, i in enumerate(col_str)]
    print('\nДанные эмпирической функции распределения:'.center(max_len)
          + '\n' + '\n'.join(
        [str(i).center(max_len) + "| " \
         + str(_func[ind]).center(6) + "" \
         for ind, i in enumerate(col_str)]))

    drawing_func = {round(key + setup * _ - 0.01 * _, 2): i for [i, [key, val]] in zip(_func, col) for _ in range(2)}
    # print(drawing_func)

    return div_arr, col, _func


def find_stat_agv(count_arr: list[list[int, int]], arr: list[int]):
    x = sum([Xi * Ni for [Xi, Ni] in count_arr]) / len(arr)
    print("Выборочное среднее x¯ или m* =", x)
    return x


def find_stat_dispersion(count_arr: list[list[int, int]], arr: list[int]):
    D = sum([Xi ** 2 * Ni for [Xi, Ni] in count_arr]) / len(arr) - (
            sum([Xi * Ni for [Xi, Ni] in count_arr]) / len(arr)) ** 2
    print('Смещённая дисперсия D* =', round(D, 4))
    print('Несмещённая дисперсия D~* =', round(D * (len(arr)) / (len(arr) - 1), 4))
    return D * (len(arr)) / (len(arr) - 1)


def pirson_kriteriy(min_max_arr: list[tuple[int, int]], div_arr: dict[float, int], x, Dv, line_arr: list[int],
                    a: float = 0.025):
    min_max_arr = [[j for j in i] for i in min_max_arr]
    sigma = Dv ** 0.5
    _s = 'i |' + \
         'границы'.center(13) + '|' + \
         'Xi - x¯'.center(13) + '|' + \
         'Zi;Z(i + 1)'.center(13) + '|' + \
         'Ф(Zi)'.center(8) + '|' + \
         'Ф(Z(i + 1))'.center(11) + '|' + \
         'P_i'.center(8) + '|' + \
         'n`_i'.center(8) + '|' + \
         'mi'.center(2) + '|' + \
         '(mi-n`i)^2'.center(10) + '|' + \
         '(mi-n`i)^2/n`i'.center(14) + '|' + \
         'ni^2/n`i'.center(8) + '|'
    print('_' * len(_s))
    print(_s)
    print('-' * len(_s))
    _sum_pi = []
    x_2_nabl = []
    m_div_n = []
    for ind, [[mi, ma], [interval, count]] in enumerate(zip(min_max_arr, div_arr.items())):
        min_max_arr[ind]: list[list[float]] = [mi, ma, (zi := round((mi - x) / sigma, 2)),
                                               (zi1 := round((ma - x) / sigma, 2))]
        if ind == 0:
            min_max_arr[ind][2] = zi = float('-inf')
        if ind + 1 == len(min_max_arr):
            min_max_arr[ind][3] = zi1 = float('inf')
        print(
            str(ind + 1).center(2) + "|" + \
            str(mi).center(6) + "|" + \
            str(ma).center(6) + "|" + \
            str(round(mi - x, 2)).center(6) + "|" + \
            str(round(ma - x, 2)).center(6) + "|" + \
            str(zi).center(6) + "|" + \
            str(zi1).center(6) + "|" + \
            str(round(stats.norm.cdf(zi) - 0.5, 4)).center(8) + "|" + \
            str(round(stats.norm.cdf(zi1) - 0.5, 4)).center(11) + "|" + \
            str(round((_p := (stats.norm.cdf(zi1) - 0.5) - (stats.norm.cdf(zi) - 0.5)), 4)).center(8) + "|" + \
            str(round(_p * 100, 2)).center(8) + "|" + \
            str(count).center(2) + "|" + \
            str(round((count - _p * 100) ** 2, 2)).center(10) + "|" + \
            str(round(_div := (count - _p * 100) ** 2 / (_p * 100), 4)).center(14) + "|" + \
            str(round(_n_div_n := (count ** 2 / (_p * 100)), 4)).center(8) + "|"
        )
        _sum_pi.append(_p * 100)
        x_2_nabl.append(_div)
        m_div_n.append(_n_div_n)
    print('¯' * len(_s))
    print('Контрольная сумма 1:', sum(_sum_pi))
    print('Контрольная сумма 2:', sum(div_arr.values()))
    print('Контрольная сумма 3:', sum(x_2_nabl))
    print('Контрольная сумма 4:', sum(m_div_n))
    print(
        f"(∑ (m_i ^ 2 / n`_i)) - n = {sum([i ** 2 / _sum_pi[ind] for ind, i in enumerate(div_arr.values())]) - len(line_arr)}")
    print(
        f"(∑ (m_i - n`_i) ^ 2) /  n`_i = {sum([(i - _sum_pi[ind]) ** 2 / _sum_pi[ind] for ind, i in enumerate(div_arr.values())])}")
    print('Число степеней свободы k =', len(div_arr) - 3)
    print('Критическая точка распределения Пирсона =', X_kr := pirson_krit[len(div_arr) - 3][a])
    print()
    print(sum(x_2_nabl), "<", X_kr, "Следовательно, распределение нормальное")


def raspr_metrics(D, x,  y=0.95, q=0.143):
    m = x
    # print(f'\nE = {y}')
    print("Так как y=0.9 в таблице отсутствует, будем использовать y=0.95")
    print("σ~в = ", D**0.5)
    print(f'Так как распределение является нормальным, то {y} = 2 * Ф(E/σ~*)')
    d = sorted([(i- y/2, i, ind/100) for ind, i in enumerate(list(stats.norm.cdf(np.linspace(0, 5, 5*100)) - 0.5))], key=lambda i: abs(i[0]))
    # print(len(d), d)
    print('E/σ~* =', d[0])
    print('E =', _E := round(d[0][-1] * (D**0.5), 4))
    print(f'Доверительный интервал для m~*: ({m - _E}; {m + _E})')
    print(f'Из таблицы при q=0.95 и n=100, q={q}')
    print(f'Тогда доверительный интервал для σ~*: ({round(D**0.5 * (1 - q), 4)}; {round(D**0.5 * (1 + q))}) ')



arr: list[str] = """
            20 26 32 34 26 28 22 30 17 24
            30 28 18 22 24 26 34 28 22 20
            34 24 28 20 32 17 22 24 26 30
            30 22 26 35 28 24 30 32 28 18
            20 30 17 24 32 28 22 26 24 30
            34 26 24 28 22 30 35 32 20 17
            28 22 36 30 20 26 28 23 24 32
            20 26 30 24 32 17 22 28 35 26
            28 35 32 22 26 24 26 24 30 24
            18 24 26 28 35 30 26 22 26 28
""".split('\n')
arr: list[list[int]] = [list(map(int, i.split())) for i in arr]
liner_arr = [j for i in arr for j in i]
count_arr: list[list[int, int]] = sorted(Counter(liner_arr).items(), key=lambda i: i[0])

print_as_table(count_arr)
div_arr, min_max_arr, _func = print_min_max(count_arr)
x = find_stat_agv(count_arr, liner_arr)
Dv = find_stat_dispersion(count_arr, liner_arr)
pirson_kriteriy(min_max_arr, div_arr, x, Dv, liner_arr)
raspr_metrics(Dv, x)

print('\n\n', "-"*30, "\nВставить в _d1 (/draw_graph/scripts/graph.js) для отрисовки графа\n", div_arr)
print('Вставить в _d2 (/draw_graph/scripts/graph.js) для отрисовки графиков\n', _func)