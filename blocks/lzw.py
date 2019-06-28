import time
import sys
import os


def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in xrange(dict_size))
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from cStringIO import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in xrange(dict_size))
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def str_builder(data):
    content = ''
    for line in data:
        content += line + '\n'
    return content


def list_to_string(data):
    content = ''
    for element in data:
        content += element + ' '


t0 = time.time()

if len(sys.argv) <= 1:
    # Demonstrate usage
    compressed = compress('TOBEORNOTTOBEORTOBEORNOT')
    #print (compressed)
    decompressed = decompress(compressed)
    #print (decompressed)
if len(sys.argv) == 2:
    file_in = sys.argv[1]
    print 'Compressing ' + file_in
    raw_data = str_builder(swap(file_in, False))
    compressed = compress(raw_data)
    decompressed = decompress(compressed)
    print 'Data Size: %d' % len(decompressed)
    print 'Compressed data size: %d' % len(compressed)
    print 'FINISHED [%ss Elapsed]' % (time.time() - t0)
