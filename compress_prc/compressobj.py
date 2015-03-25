import zlib
import binascii

compressor = zlib.compressobj()

with open('./testgzip_ori', 'r') as f:
    while True:
        block = f.read(4096)
        if not block:
            break
        compressed = compressor.compress(block)
        if compressed:
            print 'Compressed: %s' % binascii.hexlify(block)
        else:
            print 'buffering'
    remaining = compressor.flush()
    print 'Flushed: %s' % binascii.hexlify(remaining)
