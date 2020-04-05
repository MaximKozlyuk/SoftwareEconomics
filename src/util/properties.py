import csv
import os
import sys


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


class CSVFile(DefaultPath):

    def __init__(self, file_name) -> None:
        self.values = []
        super().__init__(file_name)

    def read_values(self):
        self.values = []
        with open(self.file_name) as csv_file:
            r = csv.reader(csv_file)
            for row in r:
                self.values.append(row)

    def __str__(self) -> str:
        s = ""
        for i in self.values:
            s += str(i) + "\n"
        return s
