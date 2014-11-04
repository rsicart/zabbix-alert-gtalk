#!/usr/bin/env python3

import logging
import sys, getopt

import sleekxmpp

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


	def start(self, event):

		# session start
		self.send_presence()
		self.get_roster()

		self.send_message(mto=self.recipient,
						  mbody=self.msg,
						  mtype='chat')

		# Using wait=True ensures that the send queue will be
		# emptied before ending the session.
		self.disconnect(wait=True)



if __name__ == "__main__":
	xmpp = Gtalk(sys.argv)

	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0199') # XMPP Ping

	# If you are working with an OpenFire server, you may need
	# to adjust the SSL version used:
	# xmpp.ssl_version = ssl.PROTOCOL_SSLv3

	# If you want to verify the SSL certificates offered by a server:
	# xmpp.ca_certs = "path/to/ca/cert"

	# Connect to the XMPP server and start processing XMPP stanzas.
	if xmpp.connect((xmpp.gtalk['server'], xmpp.gtalk['port'])):
		xmpp.process(threaded=False)
		print("Done")
	else:
		print("Unable to connect.")
