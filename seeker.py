# This python file uses the following encoding: utf-8

from clint.textui import colored
import os
from network_manager import NetworkManager

class Seeker:

	def __init__(self):
		print(colored.green("[*] Fetching active servers"))
		self.net_manager = NetworkManager()
		ip_list = self.net_manager.get_all_ip()
		self.ips = self.net_manager.filter_active_server(ip_list)
		print(colored.green("[+] Successfully extracted active servers."))

	def process(self, operation, data):

		if operation == 'search':
			pass
		elif operation == 'fetch':
			pass
		else:
			print(colored.red("[!] Operation not found!!"))

	def _search_net(self, tag=None, name=None, hash=None):
		# TODO:- find an efficient server search method, maybe an indexing server
		pass

	def _fetch_resource(self):
		# use requests
		pass


if __name__ == "__main__":
	pass