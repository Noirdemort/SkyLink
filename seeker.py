# This python file uses the following encoding: utf-8

from clint.textui import colored
import os
import requests
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
			self._search_net(tag=data["tag"], name=data["name"], hash_val=data["hash"])
		elif operation == 'fetch':
			self._fetch_resource(data['url'], data['filename'])
		else:
			print(colored.red("[!] Operation not found!!"))

	def _search_net(self, tag=None, name=None, hash_val=None):
		# TODO:- find an efficient server search method, maybe an indexing server
		for ip in self.ips:
			r = requests.get(f"http://{ip}:5000/search", params=(("search_tag", tag), 
																("search_name", name), 
																("search_hash", hash_val)))
			print(ip, r.text)
	
	def _fetch_resource(self, url, filename):
		r = requests.get(url)
		# Send HTTP GET request to server and attempt to receive a response

    	# If the HTTP GET request can be served
		if r.status_code == 200:
        	# Write the file contents in the response to a file specified by local_file_path
			with open(filename, 'wb') as local_file:
				for chunk in r.iter_content(chunk_size=128):
					local_file.write(chunk)


if __name__ == "__main__":
	pass