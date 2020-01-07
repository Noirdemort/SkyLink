# This Python file uses the following encoding: utf-8

import pymongo
from clint.textui import colored
from prompt_toolkit import prompt
from pathlib import Path
from magic import Magic
from hashlib import sha3_512 as sha


class Publisher:

	def __init__(self):
		mongo_url = "mongodb://localhost:27017/"
		client = pymongo.MongoClient(mongo_url)
		db = client["SkyLink"]
		self.broadcast_db = db['broadcasts']
		self.tags_db = db['tags']
		self.files_db = db['files']
	
	def process(self, content, filepath):
		if content == 'media':
			self._publish_media(filepath)
		elif content == 'markdown':
			self._publish_markdown(filepath)
		elif content == 'file':
			self._publish_file(filepath)
		elif content == 'broadcast':
			self._publish_broadcast(filepath)
		elif content == 'tag-search':
			self._tag_compiler(filepath)
		elif content == 'shred':
			self._delete(filepath)
		else:
			print(colored.red("[!] No such node."))

	def _publish_media(self, filepath):
	   self._store_file(filepath, 'media')

	def _publish_markdown(self, filepath):
		self._store_file(filepath, 'markdown')

	def _publish_file(self, filepath):
		self._store_file(filepath, 'files')

	def _publish_broadcast(self, filepath):
		print(colored.cyan('[*] Enter message to broadcast (press esc then enter to stop writing)'))
		message = prompt('>> ', multiline=True)
		self.broadcast_db.insert({"broadcast": message, 'hash': self._sha_str(message)})

	def _tag_compiler(self, filepath):
		text = open(filepath, 'r').read().strip().repalce('\n', '')
		text = text.split(' ')
		tags = list(filter(lambda x: x.startswith('#'), text))
		print(colored.cyan("\n".join(tags)))
		return {'file': filepath, 'tags': tags, 'hash': self._sha_file(filepath)}

	def _tag_store(self, tag_record):
		self.tags_db.insert(tag_record)

	def _delete(self, filepath):
		# TODO :- delete file from database also
		if self._check_file(filepath):
			Path(filepath).unlink()
			return
		print(colored.red("[!] No Such File exists!!"))

	def _store_file(self, filepath, target_file):
		if not self._check_file(filepath):
			print(colored.red("[!] No Such File exists!!"))
			return
		
		file_type = Magic().from_file(filepath)
		with open(f'{target_file}.txt', 'a') as file:
			file.write('{} :: {}\n'.format(filepath, file_type))
		
		self.files_db.insert({'file': filepath, 'hash': self._sha_file(filepath), 'type': target_file})

		if 'ASCII text' in file_type:
			tag_record = self._tag_compiler(filepath)
			self._tag_store(tag_record)
		
	def _check_file(self, filepath):
		if Path(filepath).is_file():
			return True
		return False

	def _sha_file(self, filepath):
		if not self._check_file(filepath):
			print(colored.red("[!] No Such File exists!!"))
			return
		
		shall = sha()
		with open(filepath,"rb") as f:
			for byte_block in iter(lambda: f.read(4096), b""):
				shall.update(byte_block)
			print(shall.hexdigest())
		
		return shall.hexdigest()

	def _sha_str(self, text):
		return sha(text.encode()).hexdigest()


if __name__ == '__main__':
	pass