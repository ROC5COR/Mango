from Value import Value

class MessageListener:
    
    def printMessage(self, message:str):
        print(message, end='\n')

    def printImage(self, img_path:str):
        print("[Image] "+img_path, end='\n')

    def printValue(self, value:Value):
        print(value.get_string(), end='\n')
    