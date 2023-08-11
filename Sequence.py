class Sequence:
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.values = []

    def put(self, *args):
        for v in args:
            self.values.append(v)
        if len(self.values) > self.maxLength:
            self.values = self.values[:self.maxLength]

    def getValue(self):
        return self.values


if __name__ == '__main__':
    a = Sequence(100)

