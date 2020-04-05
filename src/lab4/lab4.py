import math

from src.util.properties import PropertiesFile
from tabulate import tabulate


def round_money(x):
    return round(x, 2)


def print_money(msg, x):
    print(msg, round_money(x))


def calc_fixed_spends(arr):
    s = sum(arr)
    rows = []
    headers = ["Наименование расходов", "Сумма (руб)"]
    rows.append(headers)
    rows.append(["Накладные расходы по проекту - 10% от ФЗП АУП", arr[0]])
    rows.append(["Плановое ежемесячное гашение кредита", arr[1]])
    rows.append(["Выплата среднего банковского процента", arr[2]])
    rows.append(["Прочие расходы - 10% от накладных расходов на содержание АУП", arr[3]])
    rows.append(["ИТОГО", s])
    print(tabulate(rows, headers="firstrow", floatfmt=".2f"), "\n")
    return s


def calc_var_spends(arr):
    s = sum(arr)
    rows = []
    headers = ["Наименование расходов", "Сумма (руб)"]
    rows.append(headers)
    zp = "Основная зарплата специалистов %s процент от стоимости тиражуируемого продукта" % (round_money(arr[0]))
    rows.append([zp, arr[1]])
    rows.append(["Страховые взносы (30%) от фонда зарплаты", arr[2]])
    rows.append(["Комплектующие и расходные материалы 1% от стоимости тиражируемого продукта", arr[3]])
    rows.append(["Накладные расходы отдела маркетинга 1.5% от стоимости тиражируемого продукта% ", arr[4]])
    rows.append(["ИТОГО:", s])
    print(tabulate(rows, headers="firstrow", floatfmt=".2f"), "\n")
    return s


props = PropertiesFile("params.properties")
props = props.properties("=")

PS_cost = props[0][1]
deadline = props[1][1]
bank_credit_percent = props[2][1]
market_v = props[3][1]
additional_profit = props[4][1]
market_stuff_salary_percent = props[5][1]

one_copy_cost = PS_cost * 0.05  # стоимость тиражируемого продукта
print_money("Стоимость продажиодной копии системы:", one_copy_cost)

marketing_employ_salary = one_copy_cost * market_stuff_salary_percent

print("Таблица 2.1 Постоянные(фиксированные) расходы в месяц")
managers_overhead_spends = 50000.0 + 30000.0 + 20000.0      # накладные расходы на содержание АУП
month_credit_deposit = PS_cost / deadline
month_avg_credit_proc = (PS_cost * bank_credit_percent) / deadline
other_spends = managers_overhead_spends * 0.1
fixed_spends = calc_fixed_spends([managers_overhead_spends, month_credit_deposit, month_avg_credit_proc, other_spends])

print("Таблица 2.2 – Переменные издержки(отдел маркетинга)")
insurance_premiums = managers_overhead_spends * 0.3
comp_expendable_materials = one_copy_cost * 0.01
comp_expendable_materials_marketing = one_copy_cost * 0.015
var_spends = calc_var_spends([
    market_stuff_salary_percent,
    marketing_employ_salary,
    insurance_premiums,
    comp_expendable_materials,
    comp_expendable_materials_marketing
])

v_zero_point = fixed_spends / (one_copy_cost - var_spends)
print("Обьем выпуска, при котором достигается точка безубыточности (нулевой уровень прибыли), определяется по формуле:")
print("x0 = a / (s - b) =", math.ceil(v_zero_point))

print("\nВыводы")
print("В течении месяца фирме необходимо подготовить и продать минимум", math.ceil(v_zero_point), "копий программного"
      , "продукта по цене", round_money(one_copy_cost), "чтобы окупить постоянные и переменные расходы.")


input('\nPress ENTER to exit')
exit(0)
