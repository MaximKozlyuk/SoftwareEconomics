import math
import matplotlib.pyplot as plt
import os
import sys

from tabulate import tabulate


class DefaultPath(object):

    def __init__(self, file_name) -> None:
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the pyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            self.app_path = sys._MEIPASS
        else:
            self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.app_path = os.path.dirname(sys.argv[0])
        self.default_properties_path = self.app_path + os.path.sep + "params.properties"

        if len(file_name) != 0 and file_name != "":
            self.file_name = self.app_path + os.path.sep + file_name
        super().__init__()


class PropertiesFile(DefaultPath):

    def __init__(self, file_name) -> None:
        super().__init__(file_name)

    def properties(self, delimiter):
        p = []
        with open(self.file_name, 'r') as file:
            for row in file:
                parts = row.split(str(delimiter))
                try:
                    p.append((parts[0], float(parts[1])))
                except ValueError as e:               # to remove new line symbol in case if reading string value
                    p.append((parts[0], str(parts[1])[:len(str(parts[1]))-1]))
        return p

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

application_path = os.path.dirname(sys.argv[0])


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

# Стоимость программной системы из лб 3
PS_cost = props[0][1]
# Срок месяцев
deadline = props[1][1]
# Процент банковского кредита
bank_credit_percent = props[2][1]
# Заданный обьем рынка продаж
market_v = props[3][1]
# Дополнительная прибыль (НЕ тыс. рублей а просто рублей)
additional_profit = props[4][1]
# ЗП специалистов отдела маркетинга (%)
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

# расчет значений для графика, на 20% больше чем точка безубыточности
ceil_zero_point = math.ceil(v_zero_point)
sales_range = ceil_zero_point + (math.ceil(ceil_zero_point * 0.2)) + 1
# точки x для всех графиков одинаковы (кол-во рподанных товаров)
x_points = list(range(0, sales_range))
var_spends_counter = 0.0
var_spends_y_points = []

sales_income_counter = 0.0
sales_income_y_points = []

total_costs_counter = fixed_spends
total_costs_y_points = []
for i in range(0, sales_range):
    var_spends_y_points.append(var_spends_counter)

    sales_income_y_points.append(sales_income_counter)
    sales_income_counter += one_copy_cost

    total_costs_y_points.append(total_costs_counter)
    total_costs_counter += var_spends
    var_spends_counter += var_spends

plt.plot([0, sales_range - 1], [fixed_spends, fixed_spends], label="Постоянные издержки", color="green")
plt.plot(x_points, var_spends_y_points, label="Перменные издержки", color="brown", linestyle="dashed")
plt.plot(x_points, sales_income_y_points, label="Доходы от продаж", color="blue", linestyle="dashed")
plt.plot(x_points, total_costs_y_points, label="Общие издержки", color="brown")

zero_point_income = one_copy_cost * v_zero_point
plt.plot(
    [v_zero_point, v_zero_point], [0, zero_point_income],
    label="Точка безубыточности", color="red", linestyle="dashed"
)
plt.plot([v_zero_point], [zero_point_income], color="red", marker="o")

plt.xlabel("Количество продаж")
plt.ylabel("₽")

plt.grid()
plt.legend()
plt.show()

print("Расчет договорной цены тиражируемой системы при заданном обьеме рынка продаж")


input('\nPress ENTER to exit')
exit(0)
