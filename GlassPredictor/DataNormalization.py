

class DataNormalizer:

    def cast_to_float(self,data):
        for row in data:
            for i in range(len(row)):
                row[i]=float(row[i])
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


data = CSVparser('testset.csv')
lel = data.get_results()
print(lel)
n = DataNormalizer()
print(n.normalize_data(lel))


