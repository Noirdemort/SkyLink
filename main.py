# This Python file uses the following encoding: utf-8
import argparse
import sys

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers.system import GrammarCompleter

from clint.textui import colored

from server import Server
from publisher import Publisher
from seeker import Seeker

# FEATURES:- server, remote access and local access
#
# Panels and Comms:
#
# 1. Media Transfer p2p
# 2. Tag searching [using hash formation] (like local news, etc.)
# 3. broadcast [from handler nodes]
# 4. Message One-to-One
# 5. Localized certificates
# 6. Periodic refresh of certificates and identifying info
# 7. Encryption using certificates, generate every time, 4096 & above bits with HMAC and padding
# 8. SOS
# 9. File Server
# 10. Deniability
# 11. Creating Identity
# 12. Local security
# 13. Local verifiable trust
# 14. Master DNS
# 15. VoIP
# 16. Content Discovery


if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='skylink', description="SkyLink: Router Area Network")

	# parser.add_argument("mode", type=str, choices=["services", "publisher", "seeker"], help="Mode of operation for the skylink")

	subparsers = parser.add_subparsers(help='commands', required=True)

	# services = parser.add_argument_group(title='Services options')
	# publisher = parser.add_argument_group(title='Publisher options')
	# seeker = parser.add_argument_group(title='Seeker Options')

	services = subparsers.add_parser('services', help='SkyLink services and options')
	services.set_defaults(mode='server')
	
	publisher = subparsers.add_parser('publisher', help="SkyLink publisher and options")
	publisher.set_defaults(mode='publisher')
	
	seeker = subparsers.add_parser('seeker', help='SkyLink seeker and options')
	seeker.set_defaults(mode='seeker')

	state = services.add_mutually_exclusive_group(required=True)
	state.add_argument('--start', action='store_true', help='Start the server')
	state.add_argument('--stop', action='store_true', help='Stop the server')
	state.add_argument('--restart', action='store_true', help='Restart the server')
	state.add_argument('--set-security', action='store_true', help='Set up RSA certificates')

	publisher_control = publisher.add_mutually_exclusive_group(required=True)
	publisher.add_argument('-f', '--file', help='filepath for file in seeker mode', required=True)
	publisher_control.add_argument('--markdown', action='store_true', help='HTMl or .md Markdown files')
	publisher_control.add_argument('--object', action='store_true', help='Any general file (usually signatures or encrypted files)')
	publisher_control.add_argument('--broadcast', action='store_true', help='Broadcast message, use .txt for publishing message')
	publisher_control.add_argument('--tag-summary', action='store_true', help='get tag summary from markdown, html and text files')
	publisher_control.add_argument('--media', action='store_true', help='Media file')
	publisher_control.add_argument('--delete', action='store_true', help='Delete a certain file')

	seeker_control = seeker.add_mutually_exclusive_group(required=True)
	seeker.add_argument('--search-tag', help="Search using a particular tag")
	seeker.add_argument('--search-hash', help="Search for specific hash over the network")
	seeker.add_argument('--search-name', help="Search using a name")
	seeker.add_argument('--url', help="URL to fetch file")
	seeker.add_argument('--fname', help="Filename of downloaded file")
	seeker_control.add_argument('--search', action='store_true', help="Search a file")
	seeker_control.add_argument('--fetch', action='store_true', help="Fetch file from specific url, requires --url tag")
	seeker_control.add_argument('--news', action='store_true', help="Fetch broadcast from subnet")
	# parser.add_argument('-p', '--pid-file', default='/var/run/eg_daemon.pid')
    
	args = parser.parse_args()

	if args.mode == 'server':
		op = ""
		if args.start:
			op = 'start'
		elif args.stop:
			op = 'stop'
		elif args.restart:
			op = 'refresh'
		else:
			op = 'set_security'
		Server().process(op)

	elif args.mode == 'publisher':
		content = ""
		if args.media:
			content = "media"
		elif args.markdown:
			content = "markdown"
		elif args.broadcast:
			content = "broadcast"
		elif args.object:
			content = "file"
		elif args.delete:
			content = "shred"
		else:
			content = "tag-search"
		
		Publisher().process(content, args.file)
		
	elif args.mode == 'seeker':
		seeker = Seeker()

		if args.search:
			if not (args.search_tag or args.search_name or args.search_hash):
				print(colored.red("[!] Atleast one of tag, name or file hash is require for search"))
				exit(0)
			data = {}
			if args.search_hash:
				data["hash"] = args.search_hash
			else:
				data["hash"] = None
			
			if args.search_name:
				data["name"] = args.search_name
			else:
				data["name"] = None

			if args.search_tag:
				data["tag"] = args.search_tag
			else:
				data["tag"] = None

			seeker.process("search", data)
			
		elif args.fetch:
			if not (args.url and args.fname):
				print(colored.red("[!] Both filename and url are required."))
				exit(0)
                        
			data = {"url": args.url, "filename": args.fname}
			seeker.process("fetch", data)

		elif args.news:
			seeker.process("news", None)
		
	else:
		print(colored.red("[!] No Such Config!!"))

	sys.exit(0)
