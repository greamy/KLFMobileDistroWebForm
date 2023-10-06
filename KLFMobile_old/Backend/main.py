from ExcelHandler import ExcelFile
from QRCode import QRCode

if __name__ == "__main__":
    inputData = [["John Doe", "123 Main St", "Portage", "555-555-5555", 3, "2020-04-01", "10:00 AM"],
                 ["Aaron Smith", "456 Main St", "Kalamazoo", "555-555-5555", 2, "2020-04-01", "10:05 AM"]]
    headers = ["Name", "Address", "City", "Phone", "# in Household", "Date", "Time"]

    print("Creating or loading excel file...")
    excel = ExcelFile("Mobile Food Distribution.xlsx", headers)
    print("Adding data to excel file...")
    excel.addData(inputData)
    excel.saveFile()
    print("Excel file saved!")
