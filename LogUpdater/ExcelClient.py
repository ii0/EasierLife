import xlrd, xlwt

class ExcelClient:
    def __init__(self, sourceDir, outputDir, sourceIndex, outputHeader):
        self.sourceDir = sourceDir
        self.outputDir = outputDir
        self.source = self.getSource(sourceIndex)
        self.output = self.setOutput()
        self.storeData(outputHeader)
    def getSource(self, dataRange): # content will be the first
        with xlrd.open_workbook(self.sourceDir) as workbook:
            table = workbook.sheets()[0]
            for i in range(1, table.nrows): # ignore header
                yield [table.row_values(i)[j] for j in dataRange]
    def setOutput(self):
        workbook = xlwt.Workbook()
        table = workbook.add_sheet('metaData')
        row = 0
        while True:
            if self.outputData:
                for col in range(len(self.outputData)): table.write(row, col, self.outputData[col])
                row += 1
                workbook.save(self.outputDir)
                yield True
            else:
                yield False
    def getData(self):
        try:
            return self.source.next()
        except StopIteration:
            return None
    def storeData(self, data):
        self.outputData = data
        return self.output.next()

if __name__ == '__main__':
    ec = ExcelClient('1.xlsx', 'metaData.xls', (2, 6, 5, 0, 1), ['sender', 'time', 'receiver', 'topic', 'content'])
    for i in range(3):
        data = ec.getData()
        ec.storeData(data)

