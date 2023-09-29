import openpyxl

class ExcelFile:

    def __init__(self, fileName, headers):
        self.name = fileName
        self.headers = headers
        self.wb = self.generateFile()

    def generateFile(self):
        try:
            wb = openpyxl.load_workbook(self.name)
        except FileNotFoundError:
            wb = openpyxl.Workbook()
            wb.active.append(self.headers)

        ws = wb.active
        ws.title = self.name.split(".")[0]
        return wb

    def addData(self, data):
        ws = self.wb.active
        # check if multiple rows in data input
        if isinstance(data[0], list):
            for row in data:
                ws.append(row)
        else:
            ws.append(data)

    def saveFile(self):
        self.wb.save(self.name)
