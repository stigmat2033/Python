#!/usr/bin/python3
from M2Crypto import EVP
from optparse import OptionParser, OptionGroup
import sys

def crypt(key,iv,salt,op,infile,outfile):
    try:
        file = open(infile,'rb').read()
    except Exception:
        printError('Error opening infile {}'.format(infile))
    cipher = EVP.Cipher(alg='aes_256_cbc',key=key,iv=iv,salt=salt,op=op)
    try:
        data = cipher.update(file)
        data += cipher.final()
    except Exception:
        printError('Error proccesing file {}'.format(infile))
    try:
        file = open(outfile,'wb')
        file.write(data)
        file.close()
    except Exception:
        printError('Error writing outfile {}'.format(outfile))

def printError(data):
    """Prints data and makes sys.exit(1)"""
    print(data)
    sys.exit(1)

def printDoc(parser):
    """Prints optparser help and makes sys.exit()"""
    parser.print_help()
    sys.exit()

if __name__ == '__main__':
    usage = "usage: %prog [action] [options] arg"
    parser = OptionParser(usage=usage)
    action = OptionGroup(parser, 'Available actions',
                         'Encrypting and Decrypting actions (only one action at same time)')
    action.add_option('-e', '--encrypt', dest='enc', help='Encrypt action (default)', action='store_true', default=True)
    action.add_option('-d', '--decrypt', dest='enc', help='Decrypt action', action='store_false')
    parser.add_option_group(action)
    parser.add_option('-k', '--key', dest='key', help='Text file using as a key', type='string')
    parser.add_option('-i', '--in', dest='infile', type='string')
    parser.add_option('-o', '--out', dest='outfile', type='string')
    (options, args) = parser.parse_args(sys.argv)
    if options.key == None:
        printDoc(parser)
    if options.infile == None:
        printDoc(parser)
    if options.outfile == None:
        printDoc(parser)
    if options.enc == True:
        op = 1
    else:
        op = 0
    try:
        file = open(options.key, 'r')
    except Exception:
        printError('Error openning file {}'.format(parser.key))
    try:
        key = file.read(32).encode()
    except Exception:
        printError('Error reading 32 bites from file {}'.format(parser.key))
    try:
        iv = file.read(32).encode()
    except Exception:
        printError('Error reading 64 bites from file {}'.format(parser.key))
    try:
        salt = file.read(8).encode()
    except Exception:
        printError('Error reading 72 bites from file {}'.format(parser.key))
    file.close()
    crypt(key,iv,salt,op,options.infile,options.outfile)
