import locale
from math import ceil

locale.setlocale(locale.LC_ALL, '')

print("Lab 1 - Совокупная стоимость владения")

variant = int(input("Введите номер варианта:"), 10)

# Вариант
dataIncreaseRatio = (100 + variant) / 100.0
print("Вариант:", dataIncreaseRatio, "\n")


def roundMoney(x):
    return round(x, 2)


class Stat(object):

    def __init__(self, name, cost):
        self.name = name
        self.cost = roundMoney(cost * dataIncreaseRatio)

    def __repr__(self):
        return '{}: {}'.format(self.name, self.cost)


def var(x):
    return ceil(x * dataIncreaseRatio)


def printList(msg, l):
    print(msg)
    for i in l:
        print(i)
    print()


# Кол-во ПК в организации
pc = ceil(var(150.0))
# Кол-во пользователей в организации
users = ceil(var(170.0))
# Годовой валовой доход компании, руб.
revenue = roundMoney(75_650_000.0*dataIncreaseRatio)
# Средняя зарплата пользователя
avg_salary = roundMoney(12_000.0*dataIncreaseRatio)

IT_Budget = [
    Stat("Затраты на закупку оборудования", 400_000.0),
    Stat("Затраты на ПО", 150_000.0),
    Stat("Затраты на комплектующие", 130_000.0),
    Stat("Системный администратор - 1 ед.", 190_000.0),
    Stat("ИТ- менеджер - 1 ед.", 260_000.0),
    Stat("Программист - 1 ед.", 100_000.0),
    Stat("Персонал технической поддержки - 2 ед.", 380_000.0),
    Stat("Затраты на обучение", 70_000.0),
    Stat("Затраты на внешнюю поддержку (outsourcing)", 180_000.0),
    Stat("Затраты на разработку/внедрение ИТ- проектов", 300_000.0),
    Stat("Затраты на телефонию", 140_000.0),
    Stat("Затраты на Интернет", 100_000.0)]

print("Статистика организации: ")
print("{}: {}".format("Кол-во ПК в организации", pc))
print("{}: {}".format("Кол-во пользователей в организации", users))
print("{}: {}".format("Годовой валовой доход компании, руб.", revenue))
print("{}: {}".format("Средняя зарплата пользователя", avg_salary))

printList("IT бюджет: ", IT_Budget)

# Task 1
print("1. Рассчитать прямые ежегодные затраты на ИС.")
sumOfExpenses = sum(map(lambda x: x.cost, IT_Budget))
print("(ПЗ) Прямые ежегодные затраты на ИС:", sumOfExpenses, "\n")

# Task 2.1
print("2. Рассчитать ежегодные косвенные затраты на ИС,")
print("которые складываются из пользовательских затрат и затрат на простои системы.\n")

print("Данные для расчета затрат пользователей на ИТ:")
# Кол-во пользователей в организации
empAmount = users
print("Кол-во пользователей в организации, Кп", empAmount)
# Средняя зарплата пользователя
avgSalary = avg_salary
print("Средняя зарплата пользователя, Зп", avgSalary)
# Среднее кол-во рабочих часов в месяце
avgWorkingHoursForMonth = var(168)
print("Среднее кол-во рабочих часов в месяце, Рч", avgWorkingHoursForMonth)
# Кол-во часов в месяц, затрачиваемых одним пользователем на самообучение, обслуживание компьютера, файлов и программ
empSelfServiceForMonth = var(8)
print("Кол-во часов в месяц, затрачиваемых одним пользователем на самообучение,")
print("обслуживание компьютера, файлов и программ, Пч", empSelfServiceForMonth, "\n")

annualEmpPCCost = (avgSalary / avgWorkingHoursForMonth) * (empSelfServiceForMonth * 12)
print("2.1")
print("(Сп) Годовая стоимость деятельности пользователя в связи с наличием у него ПК:", roundMoney(annualEmpPCCost))

allEmpPCCost = annualEmpPCCost * empAmount
print("(Спг) Ежегодные затраты пользователей на ИС:", roundMoney(allEmpPCCost))

# Task 2.2
print("2.2 Данные для расчетов стоимости простоев ИТ-системы.")
shutdownForMonth = var(2)
print("Кол-во отключений системы в месяц, Ко", shutdownForMonth)
avgPowerOffDuration = var(3)
print("Средняя продолжительность отключений, часов, Чо", avgPowerOffDuration)
turnedOffUsersAmount = var(20)
print("Количество отключенных пользователей, По", turnedOffUsersAmount)
# годовой валовый доход
annualGrossIncome = roundMoney(78_880_000 * dataIncreaseRatio)
print("Годовой валовой доход компании, руб., Гд", annualGrossIncome)

# Task 2.3
print("2.3")
# Часовая оплата пользователя
mh = avgSalary / avgWorkingHoursForMonth
# Доход на каждого работника
incomePerEmp = annualGrossIncome / 12 / avgWorkingHoursForMonth / empAmount
# Простои, часов в год
inactionHoursForYear = shutdownForMonth * avgPowerOffDuration * 12

print("Часовая оплата пользователя, руб./ч:", roundMoney(mh))
print("Доход на каждого работника, руб./ч:", roundMoney(incomePerEmp))
print("Простои, часов в год:", inactionHoursForYear)

# ежегодные расходы на простои системы, руб./год
annualSystemDowntimeCost = (incomePerEmp + mh) * inactionHoursForYear * turnedOffUsersAmount

print("Ежегодные расходы на простои системы, руб./год:", roundMoney(annualSystemDowntimeCost))

indirectExpense = annualSystemDowntimeCost + allEmpPCCost
print("Общая сумма косвенных затрат:", roundMoney(indirectExpense), "\n")

# Task 3
print("3. Сложив прямые и косвенные затраты, получите итоговую сумму ТСО:")
print("Итоговая сумма ТСО: ", roundMoney(sumOfExpenses + indirectExpense))

input('Press ENTER to exit')
