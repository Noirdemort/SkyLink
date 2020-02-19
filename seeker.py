# This python file uses the following encoding: utf-8

from clint.textui import colored
import os
import requests
from network_manager import NetworkManager


class Seeker:

	'''
	Seeker class - consists of search and fetch operation from various servers in the subnet.
	Main intention of this class is to traverse the network and perform various operations in a distributed manner.
	Yet to add a way to traverse and index the whole network.
	'''

	def __init__(self):
		print(colored.green("[*] Fetching active servers"))
		self.net_manager = NetworkManager()
		ip_list = self.net_manager.get_all_ip()
		self.ips = self.net_manager.filter_active_server(ip_list)
		print(colored.green("[+] Successfully extracted active servers."))


	def process(self, operation, data):
		'''
		Receives argument from command line parser.
		:param operation - defines the type of operation to be performed. Can be search or fetch yet.
		:param data - defines resources required by the operation. handled by parser.
		'''
		if operation == 'search':
			self._search_net(tag=data["tag"], name=data["name"], hash_val=data["hash"])
		elif operation == 'fetch':
			self._fetch_resource(data['url'], data['filename'])
		elif operation == 'news':
			self._get_broadcasts()
		else:
			print(colored.red("[!] Operation not found!!"))
	

	def _search_net(self, tag=None, name=None, hash_val=None):
		'''
		Searches the subnet for files.
		:param tag - type: str, a tag for searching among text files with various hashtags.
		:param name - type: str, a name of file for searching, this parameter is least reliable
		:param hash_val - type: str, a hash for a specific file for search, return quickest result

		:return void

		'''
		# TODO:- find an efficient server search method, maybe an indexing server
        # TODO:- Switch to Async await Multithreading
		for ip in self.ips:
			r = requests.get(f"http://{ip}:5000/search", params=(("search_tag", tag), 
																("search_name", name), 
																("search_hash", hash_val)))
			print(ip, r.text)
		
	
	def _get_broadcasts(self):
		'''
		Gets broadcasts from all servers in the subnet.

		:return void
		'''
		for ip in self.ips:
			r = requests.get(f"http://{ip}:5000/newsFlash")
			print(colored.green(f"{ip} ==> {r.text}"))


	def _fetch_resource(self, url, filename):
		'''
		Fetches file from a certain server using hash value.

		:param url - type: str, url of the file to be downloaded.
		Usually of the form:- http://127.0.0.1:5000/fetch/27e82jl58ue29ol91kn11h96xb

		:param filename - type: str, file name to be used for downloaded file.

		Filename can also be full path for file to be saved.

		:return void
		'''
		r = requests.get(url)

		if r.status_code == 200:
			with open(filename, 'wb') as local_file:
				for chunk in r.iter_content(chunk_size=128):
					local_file.write(chunk)


if __name__ == "__main__":
	pass
