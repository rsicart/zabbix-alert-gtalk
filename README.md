Zabbix Alert Gtalk
==================

Alert scripts to send xmpp messages using a Gtalk account.

Settings
--------

Configure gtalk settings in a file named in the same folder settings.py.
Copy sample file settings.example.py to create it.


Usage:
------

./gtalk[2|3].py [options]

Sends an xmpp message to a recipient.

Options:
 -h | --help
 -r | --recipient
 -s | --subject
 -m | --message

Requirements (2 options)
------------------------

* python2: xmpp
* python3: sleekxmpp (via pip3 package manager, apt version is older)
