from MessageListener import MessageListener


class mango_plugin():

    def go(self, args:list, message_listener:MessageListener = MessageListener()):
        print("[Mango] Default go method")

    def get_aliases(self):
        return []

