import csv


# Обьявление классов и функций


class DefaultPath(object):

    def __init__(self, file_name, default_path) -> None:
        self.default_path = default_path
        self.file_name = self.default_path
        if len(file_name) != 0 and file_name != "":
            self.file_name = file_name
        super().__init__()


class PropertiesReading(DefaultPath):
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


class LanguageReading(DefaultPath):
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


# Инициализация параметров

langReading = LanguageReading(
    input("Введите название файла с языками (enter, для выбора по умолчанию - "
          + LanguageReading.default_languages_path + "):")
)
langReading.read_languages()

propertiesReading = PropertiesReading(
    input("Файл с параметрами для расчета (по умолчанию - "
          + PropertiesReading.default_properties_path + "):")
)
properties = propertiesReading.read_properties()

laborCategoriesDB = LaborCategoriesDB(
    input("Файл с нормативами трудоемкости разработки ПС относительно размера БД (по умолчанию - "
          + LaborCategoriesDB.default_labor_categories_path + "):")
)
laborCategoriesDB.read_categories()

# Язык программирования
language = langReading.language_by_id(properties[0][1])
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

# 1.1
# Норматив производительности труда (человеко-месяц)


# 1.2
R = 2 * N * 5 * K1 * 10 * M
print("Размерность базы данных R =", R, "полей")
laborCategory = laborCategoriesDB.labor_standard_by_size(R)
print("Норматив трудоемкости разработки ПС:", laborCategory)

# 1.3


input('\nPress ENTER to exit')
exit(0)
