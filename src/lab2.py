"""
    Фирма рассматривает целесообразность внедрения системы управления ИТ- инфраструктурой.
    По прогнозам ежегодная экономия от снижения ТСО (совокупной стоимости владения ИТ) составит 75 тыс. руб.
    Проект рассчитан на 3 года. Стартовые инвестиции в проект - 100 тыс. руб.
    Затраты на реализацию проекта составят: в 1-й год - 20 тыс. руб, во 2-й год – 15 тыс. руб., в 3-й год – 10 тыс. руб.
    Необходимо рассчитать показатели экономической эффективности проекта
    с учетом ставки дисконтирования (нормы прибыли), равной 11%.
"""

# todo input from file

import matplotlib.pyplot as plt
from sympy import *


def round_money(x_):
    return round(x_, 2)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('Линии не пересекаются')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


print("Lab2 Целесообразность внедрения системы управления ИТ- инфраструктурой\n")

print("Введите данные для расчета:")
Ic = float(input("Стартовые инвестиции:"))
inv = float(input("Ставка дисконтирования:"))
n = int(input("Горизонт расчета проекта (кол-во лет):"))
print("DP Приток средств в i-тый год:")
cashInflow = []
for i in range(0, n):
    cashInflow.append(float(input()))
print("Отток средств в i-тый год:")
cashOutflow = []
for i in range(0, n):
    cashOutflow.append(float(input()))

# 1. чистый приведенный доход NPV
CF = [-Ic]
for i in range(0, len(cashInflow)):
    CF.append(cashInflow[i] - cashOutflow[i])
print("CF:", CF)

print("Ставка дисконтирования в каждый год:")
print(inv)
NPV = 0.0
for k in range(1, len(CF)):
    NPV += (CF[k] / ((1 + inv) ** k))
    print((1.0 + inv) ** k)

NPV = round_money(NPV - Ic)
print("NPV:", NPV, "\n")

# 2. ROI
ROI = NPV * 100 / Ic
print("ROI:", ROI)

bufSum = 0
for k in range(1, n + 1):
    bufSum += CF[k] / ((1 + inv) ** k)
PI = bufSum / Ic

print("PI:", PI)

# IRR
x, y, z, t, e = symbols('x y z t e')
e = -Ic
for k in range(1, len(CF)):
    e += (CF[k] / ((1 + x) ** k))
IRR = solve(Eq(e, 0), x)[0]
print("IRR", IRR)

# 3
NPVV = [-Ic]
R = [-Ic]
for k in range(1, n + 1):
    R.append(CF[k] / ((1 + inv) ** k))
    NPVV.append(NPVV[k - 1] + R[k])

print("R:", R)
print("NPVV:", NPVV)

plt.xlabel('n, кол-во лет')
plt.ylabel('NPV')
plt.title("Чистый приведенный доход")

fig = plt.figure()
ax = fig.add_subplot(111)
xValues = list(range(0, n + 1))
plt.plot(xValues, NPVV, marker='o', label="NPV")
# plt.xticks()
plt.plot(list(range(0, n + 1)), [0] * (n + 1), color="green")
plt.grid()

# 4
balance = 0
for i in range(1, len(NPVV)):
    if NPVV[i - 1] < 0 and NPVV[i] > 0:
        balance = line_intersection(
                ((0.0, 0.0), (1.0, 0.0)),
                ((i-1, NPVV[i - 1]), (i, NPVV[i]))
        )
        print("Момент окупаемости наступит через", round(balance[0], 3), "лет")

if balance == 0:
    raise Exception("Точка окупаемости не найдена")

# 5
balanceX = balance[0], balance[0]
balanceY = (NPVV[0], NPVV[-1])
plt.plot(balance[0], balance[1], label="точка окупаемости", marker="o", color="red")
plt.text(balance[0], balance[1], round(IRR + 1, 3), horizontalalignment='right')
plt.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0.)
plt.show()

input('\nPress ENTER to exit')
exit(0)
