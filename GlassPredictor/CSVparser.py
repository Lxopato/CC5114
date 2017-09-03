import csv

class CSVparser:

    def __init__(self,file):
        self.file = file
        self.reader = list()
        self.get_file()

    def get_file(self):
        with open(self.file,'r') as f:
            self.reader = [row for row in csv.reader(f, delimiter=",")]

    def get_data(self):
        data=[]
        for row in self.reader:
            data.append(row[:-1])
        return data

    def get_results(self):
        results=[]
        for row in self.reader:
            results.append([row[-1]])
        return results