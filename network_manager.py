import os
import re
import requests

class NetworkManager:

	def __init__(self):
		pass
	
	def get_all_ip(self):
		ip_strs = list(os.popen("arp -a"))
		rt = []
		
		for ip in ip_strs:
			rt.extend(re.findall("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", ip))
		
		return list(set(rt))


	def filter_active_server(self, ip_list):
		ip = []
		for il in ip_list:
			if requests.get(f'http://{il}:5000/').text == 'SkyLink: RAreNet (Router Area Network)':
				ip.append(il)
		
		return ip
