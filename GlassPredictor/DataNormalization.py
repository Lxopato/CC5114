from GlassPredictor.CSVparser import CSVparser
class DataNormalizer:

    def cast_to_float(self,data):
        for row in data:
            for i in range(len(row)):
                row[i]=float(row[i])
        return data

    def cast_to_integer(self,data):
        for row in data:
            for i in range(len(row)):
                row[i]=int(row[i])
        return data

    def normalize_data(self,data):
        data = self.cast_to_float(data)
        for i in range(len(data[0])):
            normalized=[]
            for row in data:
                normalized.append(row[i])
            minimum = min(normalized)
            maximum = max(normalized)

            for row in data:
                row[i] = (row[i]-minimum)/(maximum-minimum)

        return data

    def data_to_binary_array(self,data):
        data = self.cast_to_integer(data)
        new=[]
        for i in range(len(data[0])):
            normalized = []
            for row in data:
                normalized.append(row[i])
            maximum = max(normalized)

            for row in data:
                aux=row[i]
                row[i] = [0 for i in range(maximum)]
                row[i][aux-1]=1

            for row in data:
                new.append(row[0])

        return new