# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass

from flask import Flask, render_template, request
from flask_caching import Cache
import os

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.secret_key = os.urandom(64)
port = int(os.environ.get('PORT', 5000))


@app.route("/")
def home():
	return "SkyLink: RAreNet (Router Area Network)"


@app.route("/media", methods=["GET", "POST"])
def media():
	if request.method == "GET":
		# list all local media
		return 'media method'
	return "media method"


@app.route("/broadcast", methods=["GET", "POST"])
def broadcast():
	if request.method == "GET":
		# list all broadcast messages
		return 'broadcast method'
	return 'broadcast method'


@app.route("/articles", methods=["GET", "POST"])
def articles():
	if request.method == "GET":
		# list all local articles
		return 'articles method'
	# extract tags and build index
	return 'articles method'
