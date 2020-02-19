# This Python file uses the following encoding: utf-8

import os
import re
import requests

class NetworkManager:

	'''
	Managers network level operations for the client.
	TODO: Will have support for encryption and more low-level security (if you can figure out what later one means)
	'''

	def __init__(self):
		pass
	
	def get_all_ip(self):
		'''
		Returns all ip(s) in the subnet.

		:return set of ip addresses in the network.
		'''
		ip_strs = list(os.popen("arp -a"))
		rt = []
		for ip in ip_strs:
			rt.extend(re.findall('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', ip))
		
		return list(set(rt))


	def filter_active_server(self, ip_list):
		'''
		Filters out ip address with active servers
		
		:param ip_list - type: list, consist of ip_addresses in the subnet

		:return list - list of ip addresses with active server
		'''
		ip = []
		for il in ip_list:
			if requests.get(f'http://{il}:5000/').text == 'SkyLink: RAreNet (Router Area Network)':
				ip.append(il)
		
		return ip
