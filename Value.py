class Value:
    def __init__(self, data, data_type:str = None, data_unit:str = None, associated_string:str = None,data_description:str=None):
        self.data = data
        self.data_type = data_type
        self.data_unit = data_unit
        self.associated_string = associated_string

    def set_data(self, data):
        self.data = data

    def get_string(self):
        if self.associated_string is None:
            return self.data
        else:
            return self.associated_string.format(str(self.data))


if __name__ == "__main__":
    v1 = Value(12, 
        data_type='int', 
        data_unit='degrees', 
        associated_string="The temperature is {}°C",
        data_description='temperature')

    print(v1.get_string())   
