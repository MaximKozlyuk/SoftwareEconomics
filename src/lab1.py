import locale
import math

locale.setlocale(locale.LC_ALL, '')

print("Lab 1 - Совокупная стоимость владения")

# Вариант
dataIncreaseRatio = 1.12
print("Вариант: 12\n")


class Expense(object):

    def __init__(self, name, cost):
        self.name = name
        self.cost = round(cost * dataIncreaseRatio)

    def __repr__(self):
        return '{}: {}'.format(self.name, self.cost)


def var(x):
    return math.floor(x * dataIncreaseRatio)


def roundMoney(x):
    return round(x, 2)


expenses = [Expense("Amount of PC", 150.0), Expense("Amount of users in organisation", 170.0),
            Expense("Gross revenue", 75_650_000.0), Expense("Average user salary", 12_000.0),
            Expense("New equipment", 400_000.0), Expense("Soft", 150_000.0), Expense("Computer parts", 130_000.0),
            Expense("System administrator", 190_000.0), Expense("IT Manager", 260_000.0),
            Expense("Programmer", 100_000.0), Expense("Tech support", 380_000.0), Expense("Trainings", 70_000.0),
            Expense("Outsourcing", 180_000.0), Expense("Development and introduction", 300_000.0),
            Expense("Phone", 140_000.0), Expense("Internet", 100_000.0)]

# Task 1
print("1. Рассчитать прямые ежегодные затраты на ИС.")
sumOfExpenses = sum(map(lambda x: x.cost, expenses))
print("Прямые ежегодные завтраты на ИС:", sumOfExpenses, "\n")

# Task 2.1
print(
    "2. Рассчитать ежегодные косвенные затраты на ИС, которые складываются из пользовательских затрат и затрат на простои системы.")
# Кол-во пользователей в организации
empAmount = var(170)
# Средняя зарплата пользователя
avgSalary = var(12000)
# Среднее кол-во рабочих часов в месяце
avgWorkingHoursForMonth = var(168)
# Кол-во часов в месяц, затрачиваемых одним пользователем на самообучение, обслуживание компьютера, файлов и программ
empSelfServiceForMonth = var(8)

annualEmpPCCost = (avgSalary / avgWorkingHoursForMonth) * (empSelfServiceForMonth * 12)
print("2.1")
print("Годовая стоимость деятельности пользователя в связи с наличием у него ПК:", roundMoney(annualEmpPCCost))

allEmpPCCost = annualEmpPCCost * empAmount
print("Ежегодные затраты пользователей на ИС:", roundMoney(allEmpPCCost))

# Task 2.2
print("2.2")
shutdownForMonth = var(2)
avgPowerOffDuration = var(3)
turnedOffUsersAmount = var(20)
# годовой валовый доход
annualGrossIncome = var(78_880_000)

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
print("Общая сумма косвенных завтрат:", roundMoney(indirectExpense), "\n")

# Task 3
print("3. Сложив прямые и косвенные затраты, получите итоговую сумму ТСО:")
print("Итоговая сумма ТСО: ", roundMoney(sumOfExpenses + indirectExpense))
