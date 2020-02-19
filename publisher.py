# This Python file uses the following encoding: utf-8

import pymongo
from clint.textui import colored
from prompt_toolkit import prompt
from pathlib import Path
from magic import Magic
from hashlib import sha3_512 as sha


class Publisher:

	'''
	Handles publishing of docuements and data from the user.

	Uses file and db for storage of data.
	'''

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
		'''
		Stores broadcast message directly in the db

		:param filepath - type: str, a .txt file containing the broadcast message
		'''
		# print(colored.cyan('[*] Enter message to broadcast (press esc then enter to stop writing)'))
		# message = prompt('>> ', multiline=True)
		message = open(filepath, 'r').read().strip()
		self.broadcast_db.insert({"broadcast": message, 'hash': self._sha_str(message)})

	def _tag_compiler(self, filepath):
		'''
		Reads file, extract tags and store them in the database

		:param filepath - type: str, path of file to be extracted

		:return dict - consist of keys ["file", "tag", "hash"]
		'''
		text = open(filepath, 'r').read().strip().replace('\n', '')
		text = text.split(' ')
		tags = list(filter(lambda x: x.startswith('#'), text))
		print(colored.cyan("\n".join(tags)))
		return {'file': filepath, 'tags': tags, 'hash': self._sha_file(filepath)}

	def _tag_store(self, tag_record):
		'''
		Store extracted tag record in the db.

		:param tag_record - type: dict, tag record to be inserted
		'''
		self.tags_db.insert(tag_record)


	def _delete(self, filepath):
		'''
		Deletes file from computer as well as database using file hash.

		:param filepath - type: str, path of file to be deleted
		'''
		if self._check_file(filepath):
			Path(filepath).unlink()
			self.files_db.delete_one({"file": filepath})
			return
		print(colored.red("[!] No Such File exists!!"))


	def _store_file(self, filepath, target_file):
		'''
		Stores file in database with its path, hash and type. Extract tags in case of ASCII text

		:param filepath - type: str, path of file to be stored
		:target_file - type: str, indicates type of file and suitable node for storage
		'''
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
		'''
		Returns if a file at a given path exists

		:param filepath - type: str, path of file to be checked for existence
		:return bool
		'''
		if Path(filepath).is_file():
			return True
		return False


	def _sha_file(self, filepath):
		'''
		Return sha3_512 hash of a given file

		:param filepath - type: str, file path

		:return str - hash of given file
		'''
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
		'''
		Return sha3_512 of given text.

		:param text - type: str, target text

		:return str - hash of given string
		'''
		return sha(text.encode()).hexdigest()


if __name__ == '__main__':
	pass
