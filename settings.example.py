#!/usr/bin/env python

gtalk = {
    'server':'',
    'port':'',
    'username':'',
    'passwd':"",
}

reply = {
    'manage': {{ vault.gtalk.replies.manage }},
    'callbackUrl': "{{ vault.gtalk.replies.callbackUrl }}",
    'timeout': {{ vault.gtalk.replies.timeout }},
}
