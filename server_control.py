# This Python file uses the following encoding: utf-8

from flask import Flask, render_template, request, send_file
from flask_caching import Cache
import os
import re
import pymongo

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.secret_key = os.urandom(64) 
port = int(os.environ.get('PORT', 5000))

mongo_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_url)
db = client["SkyLink"]
files_db = db['files']
broadcast_db = db["broadcasts"]
tags_db = db["tags"]

@app.route("/")
def home():
	'''
	Return simply a static string. Used for testing.
	'''
	return "SkyLink: RAreNet (Router Area Network)"


@app.route("/media", methods=["GET"])
def media():
	'''
	Search among media files. 
	Accepts only HTTP GET request only.
	'''
	if request.method != "GET":
		return "Method not supported. Use GET HTTP Method."
	
	files = list(files_db.find({"type" : "media"}))
	resources = "\n".join([f"{fi['hash']} :: {fi['filepath']}" for fi in files])
	return resources
	

@app.route("/broadcast", methods=["GET"])
def broadcast():
	'''
	Fetches for broadcast content.
	Accepts HTTP GET request only
	'''
	if request.method != "GET":
		return "Method not supported. Use GET HTTP Method."
	
	broadcasts = list(broadcast_db.find())
	resource = "\n".join([f'{b["message"]}' for b in broadcasts])
	return resource


@app.route("/articles", methods=["GET"])
def articles():
	'''
	Searches for ASCII text documents in the database.
	'''
	if request.method != "GET":
		return "Method not supported. Use GET HTTP Method."
	
	markdowns = list(files_db.find({"type": "markdown"}))
	tags = list(tags_db.find())
	resources = "\n".join([f"{md['hash']} :: {md['filepath']}" for md in markdowns] + 
						[f"{tg['hash']} :: {tg['filepath']}" for tg in tags])
	
	return resources


@app.route('/search', methods=['GET'])
def search():
	'''
	Performs a generic search using names, tag and hash value.

	Accepts HTTP GET request only with certain parameters:
		- search_hash: hash of file
		- search_tag: any specific tag that the file may/can contain
		- search_name: searches file with a possible filename
	'''
	if request.method != "GET":
		return "Method not supported. Use GET HTTP Method."

	files = []
	
	keyword = request.params.get("search_hash")
	if keyword:
		files.extend(_process_search(keyword))

	keyword = request.params.get("search_tag")
	if keyword:
		files.extend(_process_search(keyword))
	
	keyword = request.params.get("search_name")
	if keyword:
		files.extend(_process_search(keyword))
	
	results = "\n".join([f'{i["hash"]} {i["file"].split("/")[-1]}' for i in files])
	return results
	

@app.route('/fetch/<file_signature>', methods=['GET'])
def fetch(file_signature):
	'''
	Sends file with specific hash.
	Accepts HTTP GET request with url parameter:
		- file_signature which is a hash object
	'''
	if request.method != "GET":
		return "Method not supported. Use GET HTTP Method."

	if file_signature:
		files = _process_search(file_signature)[0]
		return send_file(files["filepath"], attachment_filename=files["filepath"].split("/")[-1])
	return "No file found!!", 404


def _process_search(keyword):
	'''
	Private method for processing search with keyword.
	:param keyword - type: str, can be a name, tag or hash

	:return list: list of records matching with keyword
	'''
	search_expr = re.compile(f".*{keyword}.*", re.I)
	search_request = {
		{'file': {'$regex': search_expr}}, 
		{'filepath': {'$regex': search_expr}}, 
		{'type': {'$regex': search_expr}}
	}

	return list(files_db.find(search_request))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)