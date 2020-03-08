"""
    Фирма рассматривает целесообразность внедрения системы управления ИТ- инфраструктурой.
    По прогнозам ежегодная экономия от снижения ТСО (совокупной стоимости владения ИТ) составит 75 тыс. руб.
    Проект рассчитан на 3 года. Стартовые инвестиции в проект - 100 тыс. руб.
    Затраты на реализацию проекта составят: в 1-й год - 20 тыс. руб, во 2-й год – 15 тыс. руб., в 3-й год – 10 тыс. руб.
    Необходимо рассчитать показатели экономической эффективности проекта
    с учетом ставки дисконтирования (нормы прибыли), равной 11%.
"""

from operator import sub
import matplotlib.pyplot as plt


def round_money(x):
    return round(x, 2)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


print("Lab2 Целесообразность внедрения системы управления ИТ- инфраструктурой\n")

# Стартовые инвестиции
Ic = 100000
# Ставка дисконтирования
i = 0.11
# Горизонт расчета проекта (кол-во лет)
n = 3
# DP Приток средств в i-тый год
cashInflow = [0, 75000, 75000, 75000]
# Z Отток средств в i-тый год
cashOutflow = [0, 20000, 15000, 10000]

# 1. чистый приведенный доход NPV
CF = list(map(sub, cashInflow, cashOutflow))
CF[0] = -Ic
print("CF:", CF)

NPV = 0.0
for k in range(1, 4):
    NPV += (CF[k] / (1 + i) ** k)
NPV = round_money(NPV - Ic)
print("NPV:", NPV, "\n")

# 2. ROI
ROI = NPV * 100 / Ic
print("ROI:", ROI)

bufSum = 0
for k in range(1, n + 1):
    bufSum += CF[k] / ((1 + i) ** k)
PI = bufSum / Ic

print("PI:", PI)

# 3
NPVV = [-Ic]
R = [-Ic]
for k in range(1, n + 1):
    R.append(CF[k] / ((1 + i) ** k))
    NPVV.append(NPVV[k - 1] + R[k])

print("R:", R)
print("NPVV:", NPVV)

plt.xlabel('n')
plt.ylabel('NPV')
plt.title("Cash flows like vine")

xValues = list(range(0, n + 1))
plt.plot(xValues, NPVV, marker='o')
plt.plot(list(range(0, n + 1)), [0] * (n + 1))

plt.legend()
plt.show()

# 4
for i in range(1, len(NPVV)):
    if NPVV[i - 1] < 0 and NPVV[i] > 0:
        print(
            line_intersection(
                ((0.0, 0.0), (1.0, 0.0)),
                ((i-1, NPVV[i - 1]), (i, NPVV[i]))
            )
        )
