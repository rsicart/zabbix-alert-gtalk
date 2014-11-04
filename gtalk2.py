#!/usr/bin/env python2

import xmpp
import sys, getopt


class Gtalk:

    def __init__(self, argv):

        # Init settings
        try:
            import settings
            gtalk = {
                'server': settings.gtalk['server'],
                'port': settings.gtalk['port'],
                'username': settings.gtalk['username'],
                'passwd': settings.gtalk['passwd'],
            }
        except:
            print("No settings file found.")
            sys.exit(1)

        self.argv = argv
        self.gtalk = settings.gtalk
        self.validateArgs(self.argv)

        self.alert = {
            'recipient':'',
            'subject':'',
            'message':'',
        }
        self.alert['recipient'] = argv[1]
        self.alert['subject'] = argv[2]
        self.alert['message'] = argv[3]


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
            usage()
            sys.exit(1)

        # check valid gtalk values
        for key, value in self.gtalk.items():
            if len(value) == 0:
                print("Invalid gtalk settings.")
                usage()
                sys.exit(4)


    def send(self):
        client = xmpp.Client(self.gtalk['username'].split('@')[1]) # only domain part
        client.connect(server=(self.gtalk['server'],5222))
        client.auth(self.gtalk['username'].split('@')[0], self.gtalk['passwd'], 'botty')
        client.sendInitPresence()
        message = xmpp.Message(self.alert['recipient'], '{}\n{}'.format(self.alert['subject'], self.alert['message']))
        message.setAttr('type', 'chat')
        client.send(message)


if __name__ == "__main__":
    g = Gtalk(sys.argv)
    g.send()
