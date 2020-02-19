# This Python file uses the following encoding: utf-8

from clint.textui import colored
from daemon import DaemonContext
from pidlockfile import PIDLockFile
from signal import SIGTERM
import os
from server_control import app, port


class Server:

	def __init__(self):
		self.current_dir = os.path.abspath(os.curdir)


	def process(self, operation):
		
		if operation == 'start':
			self._start()

		elif operation == 'stop':
			self._stop()

		elif operation == 'refresh':
			self._stop()
			self._start()
			
		elif operation == 'set_security':
			self._generate_certificates()

		else:
			print(colored.red("[!] No such command."))

	
	def _start(self):
		print(colored.green("[+] Started running server on port 5000..."))
		with DaemonContext(pidfile=PIDLockFile('{}/current.pid'.format(self.current_dir))):
			app.run(host='127.0.0.1', port=port)


	def _stop(self):
		pid = open(self.current_dir+'/current.pid', 'r').read().strip()
		pid = int(pid)
		os.kill(pid, SIGTERM)
		print(colored.green("[+] Stopped server successfully!!"))


	def _generate_certificates(self):
		os.system('openssl req -x509 -newkey rsa:8192 -nodes -out cert.pem -keyout key.pem -days 365')
		print(colored.green('[+] Certificates generated: key.pem, cert.pem'))
