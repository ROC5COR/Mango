
class MessageListener:
    
    def printMessage(self, message:str):
        print(message, end='\n')

    def printImage(self, img_path:str):
        print("[Image] "+img_path, end='\n')
