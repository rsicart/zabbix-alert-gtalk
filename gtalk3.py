#!/usr/bin/env python3

import logging
import sys, getopt

import sleekxmpp
import urllib.request
import time
import re

class Gtalk(sleekxmpp.ClientXMPP):

	def __init__(self, argv):

		# Init settings
		try:
			import settings
		except:
			print("No settings file found.")
			sys.exit(1)

		# Loglevel
		logging.basicConfig(
			level=logging.WARNING,
			format='%(levelname)-8s %(message)s'
		)

		self.argv = argv
		self.gtalk = settings.gtalk
		self.reply = settings.reply
		self.validateArgs(self.argv)

		# build alert
		self.alert = {}
		self.alert['recipient'] = self.argv[1]
		self.alert['subject'] = self.argv[2]
		self.alert['message'] = self.argv[3]

		# init client
		sleekxmpp.ClientXMPP.__init__(self, self.gtalk['username'], self.gtalk['passwd'])
		self.use_ipv6 = False
		self.recipient = self.alert['recipient']
		self.msg = "{}\n{}".format(self.alert['subject'], self.alert['message'])
		self.add_event_handler("session_start", self.start, threaded=False)
		self.add_event_handler("logout", self.logout, threaded=True, disposable=True)

		# handle responses
		if self.reply['manage']:
			self.add_event_handler("message", self.message)


	def usage(self):
			print("\nUsage: {} [options]".format(self.argv[0]))
			print("\nSends an xmpp message to a recipient.")
			print("\nOptions:")
			print(" -h | --help")
			print(" -r | --recipient")
			print(" -s | --subject")
			print(" -m | --message")
			print("\n")


	def validateArgs(self, argv):

		if len(argv) < 4:
			self.usage()
			sys.exit(1)
		
		# check valid gtalk values
		for key, value in self.gtalk.items():
			if len(value) == 0:
				print("Invalid gtalk settings.")
				self.usage()
				sys.exit(4)

		# check valid reply values
		for key, value in self.reply.items():
			if value is None or len(str(value)) == 0:
				print("Invalid reply settings.")
				self.usage()
				sys.exit(4)


	def start(self, event):

		# session start
		self.send_presence()
		self.get_roster()

		self.send_message(mto=self.recipient,
						  mbody=self.msg,
						  mtype='chat')

		# trigger logout countdown
		self.event('logout')


	def logout(self, data):
		''' Disconnect after the specified number of seconds.
		'''
		time.sleep(self.reply['timeout'])
		self.disconnect(wait=True)


	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			params = {
				'msisdn': self.getSender(msg['from']),
				'text': msg['body'],
			}
			response = self.callUrl(params)


	def getSender(self, jid):
		''' Returns the sender address of a sleekxmpp JID object.
			@params JID object
			@return string email
		'''
		return '{}@{}'.format(jid.username, jid.domain)


	def callUrl(self, params):
		''' Makes an http request with params as querystring.
			@params dict of get parameters
			@return string
		'''
		querystring = urllib.parse.urlencode(params)
		data = urllib.request.urlopen('{}?{}'.format(self.reply['callbackUrl'], querystring)).read()
		return data


if __name__ == "__main__":
	xmpp = Gtalk(sys.argv)

	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0199') # XMPP Ping

	# Connect to the XMPP server and start processing XMPP stanzas.
	if xmpp.connect((xmpp.gtalk['server'], xmpp.gtalk['port'])):
		xmpp.process(block=False)
		print("Done")
		sys.exit(0)
	else:
		print("Unable to connect.")
		sys.exit(1)
