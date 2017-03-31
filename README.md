# Cracking LDAP

## slappasswd-cracker

A proof of concept to demonstrate cracking SSHA-hashed LDAP password.

OpenLDAP uses SSHA (RFC 2307) to store password in its database, under `userPassword` attribute.

What is SSHA ? SSHA is basically `SHA1(clear_text + salt) + salt`. OpenLDAP then encode the SSHA value using Base-64 and prepend "{SSHA}" in front of it.

**The last 4 bytes of an SSHA hash is the salt.**

In other words, if the value of `userPassword` is known, it is possible to extract the salt, and perform brute-force or rainbow attack to discover the plain text.

What can we do with this knowledge ?

One purpose is to perform password auditing. Password policy can be enforced in OpenLDAP setup to prevent weak password based on patterns. However, no password policy is perfect. The policy may not protect against commonly-used passwords, or a password that is reused from other accounts within the same company.

**Code explanation:**

Suppose we know a `userPassword` value.

```
ldapUserPassword = "{SSHA}rj5qElfD1JK7PCKSLZzxIldkREeFW2Dv" # "tony"
```

Extract the salt.

```
ldapUserPassword_b64decoded = base64.b64decode(ldapUserPassword) # base64 decode the LDAP's userPassword

salt_str = ldapUserPassword_b64decoded[-4:] # because this is SSHA: the last 4 bytes is the salt!
```

A brute force attempt.

```
challenge_clear = "tony" # A bad guy says: "OK let me guess the password..."
```

Rebuild the hash using the same algorithm that OpenLDAP uses.

```
challenge_salted = challenge_clear + salt_str # Sprinkle the salt..

challenge_sha1 = hashlib.sha1(challenge_salted).digest() # hash it ...

challenge_complete = "{SSHA}" + base64.encodestring(challenge_sha1 + salt_str) # append with the original salt, and base64 encode it!
```

Result:

```
print "%s vs %s" % (ldapUserPassword, challenge_complete) # Ta-da!

Output:
{SSHA}rj5qElfD1JK7PCKSLZzxIldkREeFW2Dv vs {SSHA}rj5qElfD1JK7PCKSLZzxIldkREeFW2Dv
```

## Improvements

- Use Perl which might be faster

- Find GPU-bound library and run on GPU-optimized machines, which will be even faster

- The faster it is, the more viable it is for a comprehensive testing

## Road map

Version 1: Able to run password verification
Version 2: Able to use GPU to run the hashlib.sha1.digest()
Version 3: Able to parellel multiple "threads" to GPU
Version 4: Able to parellel CPU threads and GPU threads
Version 5: Able to queue so that multiple machine can run it parellel
