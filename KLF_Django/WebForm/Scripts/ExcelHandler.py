import openpyxl
import os

class ExcelFile:

	def __init__(self, file_name, headers, directory):
		self.name = file_name
		self.headers = headers
		self.directory = directory
		self.file_path = os.path.join(directory, file_name)
		self.wb = self.generate_file()
	
	def generate_file(self):
		# Assuming 'ExcelDocs' is the subdirectory you want to save the Excel file in
		#directory = 'WebForm/ExcelDocs'
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

		file_path = os.path.join(self.directory, self.name)
		if os.path.exists(file_path):
			wb = openpyxl.load_workbook(file_path)
		else:
			wb = openpyxl.Workbook()
			ws = wb.active
			ws.append(self.headers)
			wb.save(file_path)
			wb = openpyxl.load_workbook(file_path)

		ws = wb.active
		ws.title = self.name.split(".")[0]
		return wb

	def add_data(self, data):
		ws = self.wb.active
		# check if multiple rows in data input

		if isinstance(data[0], list):
			for row in data:
				ws.append(row)
		else:
			ws.append(data)

	def save_file(self):
		self.wb.save(self.file_path)

	def delete_file(self):
		os.remove(self.file_path)

	def get_file(self):
		return open(self.file_path, 'rb')
