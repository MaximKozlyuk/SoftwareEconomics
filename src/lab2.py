"""
    Фирма рассматривает целесообразность внедрения системы управления ИТ- инфраструктурой.
    По прогнозам ежегодная экономия от снижения ТСО (совокупной стоимости владения ИТ) составит 75 тыс. руб.
    Проект рассчитан на 3 года. Стартовые инвестиции в проект - 100 тыс. руб.
    Затраты на реализацию проекта составят: в 1-й год - 20 тыс. руб, во 2-й год – 15 тыс. руб., в 3-й год – 10 тыс. руб.
    Необходимо рассчитать показатели экономической эффективности проекта
    с учетом ставки дисконтирования (нормы прибыли), равной 11%.
"""
from operator import sub
print("Lab2 Целесообразность внедрения системы управления ИТ- инфраструктурой")

initialInvestments = 100000
i = 0.11
n = 3
# DP
cashInflow = [0, 75000, 75000, 75000]
# Z
cashOutflow = [0, 20000, 15000, 10000]

# 1. NPV
CF = list(map(sub, cashInflow, cashOutflow))
CF[0] = -initialInvestments
print("CF:", CF)

NPV = 0.0
for k in range(1, 4):
    NPV += (CF[k] / (1 + i) ** k)
NPV -= initialInvestments
print("NPV:", NPV)

# 2. ROI

ROI = NPV * 100 / initialInvestments
print("ROI:", ROI)

bufSum = 0
for k in range(1, n+1):
    bufSum += CF[k] / (1 + i) ** k
PI = bufSum / initialInvestments

print("PI:", PI)

# 3
NPVV = [-initialInvestments]
R = [-initialInvestments]
for k in range(1, n+1):
    R.append(CF[k] / ((1 + i) ** k))
    NPVV.append(NPVV[k-1] + R[k])

print("R:", R)
print("NPVV:", NPVV)

