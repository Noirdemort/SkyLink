from clint.textui import colored

class Seeker:
    
    def __init__(self):
        pass

    def process(self, operation, data):

        if operation == 'search':
            pass
        elif operation == 'fetch':
            pass
        else:
            print(colored.red("[!] Operation not found!!"))
    
    def _search_net(self, tag=None, name=None, hash=None):
        pass
    
    def _fetch_resource(self):
        pass