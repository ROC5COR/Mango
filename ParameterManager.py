import json
import os
import logging

logger = logging.getLogger()

class ParamameterManager:
    def __init__(self, identity, file_path):
        self.config = dict()
        self.config_file = file_path
        self.identity = identity

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                self.config = json.load(f)
                #print("File loaded")
                f.close()
        else:
            logger.warning("[ParameterManager] The file "+file_path+" does not exists")

    def write_to_disk(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, sort_keys=True, indent=4)
            f.close()

    def set_param(self, key:str, value):
        self.config[str(self.identity)+"."+key] = value

    def get_param(self, key, default_value):
        value = None
        try:
            value = self.config[str(self.identity)+"."+key]
            return value
        except:
            None

        self.set_param(key, default_value) # Create the key in the file
        self.write_to_disk()
        return default_value
            

if __name__ == '__main__':
    print("Starting")
    param = ParamameterManager('main', 'config.json')
    print("key1: "+str(param.get_param('key1',None)))
    print("key2: "+str(param.get_param('key2',None)))
    print("key3: "+str(param.get_param('key3',None)))

    param.set_param('key1', {'city':'grenoble', 'temperature':12})
    param.set_param('key3', ['1', '2', '3'])
    param.write_to_disk()
