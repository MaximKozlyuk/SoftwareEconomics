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
        super().__init__(file_name, self.default_languages_path)

    def read_languages(self):
        l = []
        with open(self.file_name) as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                l.append(Language(int(row[0]), row[1], float(row[2]), float(row[3])))
        return l


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


# Инициализация параметров

langReading = LanguageReading(
    input("Введите название файла с языками (enter, для выбора по умолчанию - "
          + LanguageReading.default_languages_path + "):")
)
languages = langReading.read_languages()

propertiesReading = PropertiesReading(
    input("Введите название файла с параметрами для расчета (по умолчанию - "
          + PropertiesReading.default_properties_path + "):")
)
properties = propertiesReading.read_properties()

# Язык программирования
language = None
for i in range(0, len(languages)):
    if languages[i].lang_id == properties[0][1]:
        language = languages[i]
# Срок разработки (мес.)
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


input('\nPress ENTER to exit')
exit(0)
