from Crypto.Cipher import AES
import base64
import utils
import sys
import os

# the block size for the cipher object; must be 16 per FIPS-197
BLOCK_SIZE = 16
PADDING = '{'

# pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

if '-e' in sys.argv:
    # generate a random secret key
    secret = os.urandom(BLOCK_SIZE)
    # create a cipher object using the random secret
    cipher = AES.new(secret)
    # encode a string
    encoded = EncodeAES(cipher, sys.argv[2])
    os.system('echo '+encoded+' >> encrypted.txt')
    os.system('echo '+base64.b64encode(secret)+' >> key.txt')

if '-d' in sys.argv:
    # generate a random secret key
    secret = base64.b64decode(utils.swap('key.txt',False).pop())
    encoded = utils.swap('encrypted.txt', False).pop()
    # create a cipher object using the random secret
    cipher = AES.new(secret)
    # decode the encoded string
    decoded = DecodeAES(cipher, encoded)
    print 'Result:', decoded

if 'clear' in sys.argv:
    os.remove('key.txt')
    os.remove('encrypted.txt')
