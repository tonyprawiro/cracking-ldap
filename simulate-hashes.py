import hashlib
import base64
import datetime
import sys

# Load passwords from word list. Extract word-list.txt.tar.bz2 and put the text
# file in the same directory as this script
print "Loading word list..."
with open("word-list.txt") as f:
    combinations = f.readlines()
combinations = [x.strip() for x in combinations]
count = len(combinations)
print "done."

print "Performing hashes: "

salt_str = "1234" # dummy salt
default_pw_start = datetime.datetime.now()

for i in xrange(0, count):

    # Hashing steps
    challenge_clear = combinations[i]
    challenge_salted = challenge_clear + salt_str
    challenge_sha1 = hashlib.sha1(challenge_salted).digest()
    challenge_complete = "{SSHA}" + base64.encodestring(challenge_sha1 + salt_str)

    # Show progress
    if i>0 and i % 1000000 == 0:
        sys.stdout.write("%dm " % (i/1000000))

print ""

default_pw_end = datetime.datetime.now()
default_pw_time = default_pw_end - default_pw_start

print "done in %d seconds" % default_pw_time.total_seconds()
