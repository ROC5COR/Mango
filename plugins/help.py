import mango
import os

def instance():
    return Help()

class Help():
    def go(self,args: list):
        print("Modules present :")
        raw_file_list = os.listdir(mango.plugins_path)
        for raw_file in raw_file_list:
            if raw_file.endswith('.py'):
                print("\t- "+str(raw_file[:-3]))
