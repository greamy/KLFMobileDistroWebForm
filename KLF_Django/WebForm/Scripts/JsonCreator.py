import json

class JsonHandler:

    def __init__(self, in_file):
        self.in_file = in_file
        self.json_object = self.loadJson()

    def loadJson(self):
        with open(self.in_file) as json_file:
            json_object = json.load(json_file)
            print(json_object)
            print(type(json_object))
        return json_object

    def addData(self, data):
        if type(data) == dict:
            # for each key in data, add the values to the json object without overwriting any existing data with the same key
            for key in data:
                if key not in self.json_object:
                    self.json_object[key] = data[key]
                else:
                    self.json_object[key].extend(data[key])
        else:
            print("JsonHandler Error: Data must be a dictionary")
            return -1
        return self.json_object


    def saveJson(self, fileName):
        with open(fileName, 'w') as outfile:
            json.dump(self.json_object, outfile, indent=4)
        return fileName