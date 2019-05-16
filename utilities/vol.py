import os
import sys


def import_handler(package):
    os.system('yes | pip install '+package+';clear')
    print '\033[1mInstalled \033[34m'+package+'\033[0m'
    return True


try:
    import base64
    foundB64 = True
except ImportError:
    import_handler('base64')
    import base64
try:
    from Crypto.Cipher import AES
    foundAES = True
except ImportError:
    import_handler('PyCrypto')
    from Crypto.Cipher import AES
try:
    import time
except ImportError:
    import_handler('time')
    import time
'''                                 END OF IMPORTs                                    '''
# ====================================UTIL_FCNs========================================== #


def ap_discovery(iface):
    t0 = time.time()
    find_aps = 'iw '+iface+' scan | grep "SSID:*" | cut -b 8-20 >> ssids.txt'
    os.system(find_aps)
    networks = []
    for ap in swap('ssids.txt', True):
        if ap not in networks and len(list(ap))>=1:
            networks.append(ap)
    if 'ID List' in networks:
        networks.remove('ID List')
    return networks


def swap(fname,destroy):
    data = []
    for line in open(fname,'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def file_encrypt(fname, destroy):
    BSZ = 16
    PADDING = '{'
    # DEFINE PADDING FUNCTION
    PAD = lambda s: s + (BSZ - len(s) % BSZ) * PADDING
    # EXTRACT FILE's CLEAR_TEXT
    content = ''
    for element in open(fname, 'r').readlines():
        content += element
    if destroy:
        os.remove(fname)
    # GET SOME RANDOM BYTES AND ENCRYPT
    secret = os.urandom(BSZ)
    if foundAES and foundB64:
        c = AES.new(secret)
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(PAD(s)))
        encrypted_data = EncodeAES(c, content)
        open('enc.txt', 'w').write(encrypted_data)
    return secret


def file_decrypt(fname, destroy, key):
    PADDING = '{'
    # EXTRACT FILE's CLEAR_TEXT
    content = ''
    for element in open(fname, 'r').readlines():
        if element.split(' ')[0] == '\n ':
            content += element
        else:
            content += element + ' '
    if destroy:
        os.remove(fname)
    if foundAES and foundB64:
        c = AES.new(key)
        DecodeAES = lambda c, s: c.decrypt(base64.b64decode(s)).rstrip(PADDING)
        return DecodeAES(c, content)

# ======================================================================================= #


def main():
    # A Demonstration of taking a program, deleting/encrypting it, and
    #    # Then proceeding to decrypt and execute successfully
    if 'demo' in sys.argv:
        prog = 's3c.py'
        key = file_encrypt(prog, True)
        clear_prog = file_decrypt('enc.txt', True, key)
        ln1 = clear_prog.split('\n')[0]
        rest = clear_prog.split(ln1)[1:]

        os.system('ls; sleep 3')
        print 'Creating Program from encrypted BLOB'
        open('program.py', 'w').write(clear_prog)
        print 'Attempting to run decrypted program'
        os.system('python program.py run')
        os.system('rm program.py')
        print '===================== FINISHED ======================'


if __name__ == '__main__':
    main()
