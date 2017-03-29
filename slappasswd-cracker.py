#!/bin/bash

"""
$ slappasswd
New password: tony
Re-enter new password: tony
{SSHA}rj5qElfD1JK7PCKSLZzxIldkREeFW2Dv

$ echo "rj5qElfD1JK7PCKSLZzxIldkREeFW2Dv" | base64 -D | hexdump -C

00000000  ae 3e 6a 12 57 c3 d4 92  bb 3c 22 92 2d 9c f1 22  |.>j.W....<".-.."|
00000010  57 64 44 47 85 5b 60 ef                           |WdDG.[`.|
00000018
"""

import hashlib
import base64

ldapUserPassword = "{SSHA}rj5qElfD1JK7PCKSLZzxIldkREeFW2Dv" # "tony"

ldapUserPassword_b64decoded = base64.b64decode(ldapUserPassword) # base64 decode the LDAP's userPassword

salt_str = ldapUserPassword_b64decoded[-4:] # because this is SSHA: the last 4 bytes is the salt!

challenge_clear = "tony" # A bad guy says: "OK let me guess the password..."

challenge_salted = challenge_clear + salt_str # Sprinkle the salt..

challenge_sha1 = hashlib.sha1(challenge_salted).digest() # hash it ...

challenge_complete = "{SSHA}" + base64.encodestring(challenge_sha1 + salt_str) # append with the original salt, and base64 encode it!

print "%s vs %s" % (ldapUserPassword, challenge_complete) # Ta-da!
