import csv
import math
from tabulate import tabulate


# Обьявление классов и функций


class DefaultPath(object):

    def __init__(self, file_name, default_path) -> None:
        self.default_path = default_path
        self.file_name = self.default_path
        if len(file_name) != 0 and file_name != "":
            self.file_name = file_name
        super().__init__()


class PropertiesFile(DefaultPath):
    default_properties_path = "./lab3/params.properties"

    def __init__(self, file_name) -> None:
        super().__init__(file_name, self.default_properties_path)

    def read_properties(self):
        p = []
        with open(self.file_name, 'r') as file:
            for row in file:
                parts = row.split("=")
                p.append((parts[0], float(parts[1])))
        return p


class LanguagesFile(DefaultPath):
    # todo переделать в ./languages.csv протестить работоспособность в виде exe-шника
    default_languages_path = "./lab3/languages.csv"

    def __init__(self, file_name) -> None:
        self.languages = []
        super().__init__(file_name, self.default_languages_path)

    def read_languages(self):
        l = []
        with open(self.file_name) as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                l.append(Language(int(row[0]), row[1], float(row[2]), float(row[3])))
        self.languages = l
        return l

    def language_by_id(self, lang_id):
        for l in self.languages:
            if l.lang_id == lang_id:
                return l
        return None


class Language(object):

    def __init__(self, lang_id, name, asm_loc, loc) -> None:
        self.lang_id = lang_id
        self.name = name
        self.asm_loc = asm_loc
        self.loc = loc
        super().__init__()

    def __str__(self) -> str:
        return self.__class__.__name__ + " " + str(self.lang_id) + " " + self.name \
               + " " + str(self.asm_loc) + " " + str(self.loc)


class LaborCategoriesDB(DefaultPath):
    default_labor_categories_path = "./lab3/labor_categories_db.csv"

    def __init__(self, file_name) -> None:
        self.categories = []
        self.size = 0
        super().__init__(file_name, self.default_labor_categories_path)

    def labor_standard_by_size(self, db_size):
        for i in self.categories:
            if i[0] <= db_size < i[1]:
                return i
        return None

    def read_categories(self):
        self.categories = []
        with open(self.file_name) as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                self.categories.append(
                    (int(row[0]), int(row[1]), float(row[2]))
                )


class Method(object):
    all = []
    allNames = []

    def __init__(self, name, T, Z) -> None:
        self.name = name
        self.T = T
        self.Z = Z
        Method.all.append(self)
        Method.allNames.append(name)
        super().__init__()

    @staticmethod
    def optimal():
        opt = Method.all[0].T
        for i in Method.all:
            if i.T < opt:
                opt = i
        return opt

    def __str__(self) -> str:
        return self.name + " " + str(round(self.T, 4)) + " " + str(math.ceil(self.Z))


class LifeCircleStage(object):

    # alpha - трудозатраты, beta - длительность
    def __init__(self, lf_id, name, alpha, beta, analyst, programmers, tech_stuff) -> None:
        self.lf_id = lf_id
        self.name = name
        self.alpha = alpha
        self.beta = beta
        # процентное распределение специалистов по этапам жизненного цикла
        self.analyst = analyst
        self.programmers = programmers
        self.tech_stuff = tech_stuff
        super().__init__()

    def __str__(self) -> str:
        return "Этап ЖЦ " + str(self.lf_id) + " " + self.name + " a = " + str(self.alpha) + " b = " + str(self.beta) + \
               " " + str(self.analyst) + " " + str(self.programmers) + " " + str(self.tech_stuff)


class LifeCircleStagesFile(DefaultPath):
    default_lc_path = "./lab3/life_circle_stage.csv"

    def __init__(self, file_name) -> None:
        self.lc_stages = []
        self.emp_by_lc = []
        self.z_i = []
        self.d_i = []
        self.the_salary_fund = []
        super().__init__(file_name, self.default_lc_path)

    def read_life_circles(self):
        self.lc_stages = []
        with open(self.file_name) as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                self.lc_stages.append(
                    LifeCircleStage(int(row[0]), row[1], float(row[2]), float(row[3]),
                                    float(row[4]), float(row[5]), float(row[6]))
                )

    # Расчитывает и печатает таблицу 1.7
    def avg_emp_amount(self, T, D):
        headers = ["Этапы жизненного цикла", "Численность Zi(чел)", "Длительность, месяцов Дi"]
        self.z_i = []
        self.d_i = []
        rows = [headers]
        for stage in self.lc_stages:
            self.z_i.append(math.ceil(stage.alpha * T / stage.beta * D))
            self.d_i.append(stage.beta * D)
            rows.append([stage.name, self.z_i[-1], self.d_i[-1]])
        print(tabulate(rows, headers="firstrow"))
        return self.z_i, self.d_i

    # Расчитывает и печатает таблицу 1.9
    def emp_amount_by_life_circle(self):
        self.emp_by_lc = []
        headers = ["Этапы жизненного цикла", "Аналитики", "Программисты", "Технические специалисты"]
        rows = [headers]
        for i in range(len(self.lc_stages)):
            self.emp_by_lc.append(
                [math.ceil(self.lc_stages[i].analyst * self.z_i[i]),
                 math.ceil(self.lc_stages[i].programmers * self.z_i[i]),
                 math.ceil(self.lc_stages[i].tech_stuff * self.z_i[i])]
            )
            row = [self.lc_stages[i].name]
            row.extend(self.emp_by_lc[i])
            rows.append(row)
        print(tabulate(rows, headers="firstrow"))

    # Расчитывает и печатает таблицу 1.10
    def salary_fund(self, programmer_rate_, analyst_ratio, tech_ratio):
        self.the_salary_fund = []
        headers = ["Этапы жизненного цикла", "Аналитики", "Программисты", "Техник", "ФЗП по этапу"]
        rows = [headers]
        # определяем месячные ставки:
        analyst_rate = programmer_rate_ * analyst_ratio
        tech_rate = programmer_rate * tech_ratio
        # считаем зарплаты
        all_salary_sum = 0.0
        for i in range(len(self.lc_stages)):
            row = [self.lc_stages[i].name]  # добавляем название этапа жц
            self.the_salary_fund.append([
                analyst_rate * self.d_i[i] * self.emp_by_lc[i][0],
                programmer_rate * self.d_i[i] * self.emp_by_lc[i][1],
                tech_rate * self.d_i[i] * self.emp_by_lc[i][2]
            ])
            row.extend(self.the_salary_fund[-1])  # добавляем расчитанные зп на этапе
            stage_sum = sum(self.the_salary_fund[-1])
            all_salary_sum += stage_sum
            self.the_salary_fund.append(stage_sum)
            row.append(stage_sum)  # сумма ФЗП
            rows.append(row)
        print(tabulate(rows, headers="firstrow", floatfmt=".2f"))
        return all_salary_sum


# Инициализация параметров

languages = LanguagesFile(
    input("Введите название файла с языками (enter, для выбора по умолчанию - "
          + LanguagesFile.default_languages_path + "):")
)
languages.read_languages()

propertiesReading = PropertiesFile(
    input("Файл с параметрами для расчета (по умолчанию - "
          + PropertiesFile.default_properties_path + "):")
)
properties = propertiesReading.read_properties()

laborCategoriesDB = LaborCategoriesDB(
    input("Файл с нормативами трудоемкости разработки ПС относительно размера БД (по умолчанию - "
          + LaborCategoriesDB.default_labor_categories_path + "):")
)
laborCategoriesDB.read_categories()

lifeCircleStagesFile = LifeCircleStagesFile(
    input("Файл с распределением трудозатрат по жизненным циклам ПС (по умолчанию - "
          + LifeCircleStagesFile.default_lc_path + "):")
)
lifeCircleStagesFile.read_life_circles()

# Язык программирования
language = languages.language_by_id(properties[0][1])
# Срок разработки Д (мес.)
deadline = properties[1][1]
# Размерность системы определенная экспертами
system_size = properties[2][1]
# БД - N
N = properties[3][1]
# БД - K1
K1 = properties[4][1]
# БД - M
M = properties[5][1]
# Кол-во функциональных точек
func_points = properties[6][1]
# V - коэфф. внешней среды
V = properties[7][1]
# Ставка программиста (руб.)
programmer_rate = properties[8][1]
# Отношения ставки программиста к:
# системному аналитику
programmerToAnalystSalary = float(properties[9][1])
# техническому специалисту
programmerToTechStuff = float(properties[10][1])

print("Выбранный тип программной системы: ИСС")

# 1.1
print("\n1.1 Прямой метод определения технико-экономических показателей (метод экспертных оценок)")
P = 0.0
if system_size < 30000:
    P = 220
else:
    P = 160
print("Норматив производительности труда (строк/человеко-месяц) P =", P)
T_1 = system_size / P
print("Трудозатраты на разработку системы:", T_1)
Z_1 = T_1 / deadline
print("Средняя численность специалистов: Z =", math.ceil(Z_1))
method1 = Method("Прямой метод (экспертных оценок)", T_1, Z_1)

# 1.2
print("\n1.2 Метод определения ТЭП проекта на основе размерности БД программной системы.")
R = 2 * N * 5 * K1 * 10 * M
print("Размерность базы данных R =", int(math.ceil(R)), "полей")
laborCategory = laborCategoriesDB.labor_standard_by_size(R)
print("Норматив трудоемкости разработки ПС: [", laborCategory[0], ",", laborCategory[1], "] ϴ‎ =", laborCategory[2])
T_2 = 0.01 * R * laborCategory[2]
print("Трудозатраты: ", T_2)
Z_2 = T_2 / deadline
print("Средняя численность специалистов:", math.ceil(Z_2))
method2 = Method("На основе размерности БД", T_2, Z_2)

# 1.3
print("\n1.3 Определение технико-экономических показателей функциональных точек")
W = 0.65 + (0.01 * V)
print("Влияние факторов внешней среды на общее кол-во функциональных точек W =", W)
Rf = func_points * W
print("Уточненное кол-во функ. точек с учетом факторов внешней среды R(F) =", Rf)
R_LOC = Rf * language.loc
print("Размерность ПО для", language.name, ":", R_LOC)
COCOMO_A = 3
COCOMO_E = 1.12
T_3 = COCOMO_A * ((R_LOC / 1000) ** COCOMO_E) / 12
print("Трудозатраты (выбрана ИСС): ", T_3)
Z_3 = T_3 / deadline
print("Средняя численность специалистов:", math.ceil(Z_3), "\n")
method3 = Method("Функциональных точек", T_3, Z_3)

print("Выводы")
table = [
    ["Метод", "Трудозатраты (чм)", "Деятельность (мес)", "Исполнителей (чел)"],
    [Method.allNames[0], T_1, deadline, math.ceil(Z_1)],
    [Method.allNames[1], T_2, deadline, math.ceil(Z_2)],
    [Method.allNames[2], T_3, deadline, math.ceil(Z_3)]
]
print(tabulate(table, headers="firstrow"))

optMethod = Method.optimal()
print("\n1.4 Пределение стоимости (договорной цены) на создание ПС")
print("Выбираем исходные данные, полученные при помощи метода:",
      optMethod, "как наименее затратные")

print("\nТаблица 1.7 Расчет средней численности сотрудников")
Zi, Di = lifeCircleStagesFile.avg_emp_amount(optMethod.T, deadline)

print("\nТаблица 1.9 Расчет численности специалистов по этапам жизненного цикла")
lifeCircleStagesFile.emp_amount_by_life_circle()

print("\nТаблица 1.10 Распределение фонда заработной платы по этапам жизненного цикла ПС")
print("\nФонд оплаты труда на разработку и коплексные испытания системы составляет:",
      round(
          lifeCircleStagesFile.salary_fund(programmer_rate, programmerToAnalystSalary, programmerToTechStuff), 2
      ), "рублей")

input('\nPress ENTER to exit')
exit(0)
