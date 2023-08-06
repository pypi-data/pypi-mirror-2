#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Loic Jaquemet loic.jaquemet+python@gmail.com
#

__author__ = "Loic Jaquemet loic.jaquemet+python@gmail.com"

import os,logging,sys, argparse

import ctypes
import ctypes_openssl,ctypes_openssh

from ctypes import * # TODO delete
from ptrace.ctypes_libc import libc
from haystack.abouchet import StructFinder
from haystack.memory_mapper import MemoryMapper
from output import FileWriter

# linux only
from ptrace.debugger.debugger import PtraceDebugger
from ptrace.debugger.memory_mapping import readProcessMappings

log=logging.getLogger('openssl')

from ctypes.util import find_library
_libssl = find_library('ssl')
_libssl = ctypes.cdll.LoadLibrary(_libssl)


class RSAFileWriter(FileWriter):
  def __init__(self,folder='outputs'):
    FileWriter.__init__(self,'id_rsa','key',folder)
  def writeToFile(self,instance):
    prefix=self.prefix
    '''
    PEM_write_RSAPrivateKey(f, rsa_p, None, None, 0, None, None)
    PEM_write_RSAPrivateKey(fp,x, [enc,kstr,klen,cb,u]) 
     -> PEM_ASN1_write((int (*)())i2d_RSAPrivateKey,PEM_STRING_RSA,fp, (char *)x, [enc,kstr,klen,cb,u])
    int PEM_ASN1_write(i2d_of_void *i2d, const char *name, FILE *fp, char *x, [const EVP_CIPHER *, unsigned char *kstr,int , pem_password_cb *, void *])
     -> PEM_ASN1_write_bio(i2d, name, b, x  [,enc,kstr,klen,callback,u] );
    int PEM_ASN1_write_bio(i2d_of_void *i2d, const char *name, BIO *bp, char *x ,  [..]
     -> i2d_RSAPrivateKey( sur x )
      -> ASN1_item_i2d_bio(ASN1_ITEM_rptr(RSAPrivateKey), bp, rsa);
       -> i=BIO_write(out,&(b[j]),n);
     -> i=PEM_write_bio(bp,name,buf,data,i);
     
    en gros, c'est ctypes_openssl.RSA().writeASN1(file)
    '''
    filename=self.get_valid_filename()
    f=libc.fopen(filename,"w")  
    ret=_libssl.PEM_write_RSAPrivateKey(f, ctypes.byref(instance), None, None, 0, None, None)
    libc.fclose(f)
    if ret < 1:
      log.error("Error saving key to file %s"% filename)
      return False
    log.info ("[X] Key saved to file %s"%filename)
    return True

class DSAFileWriter(FileWriter):
  def __init__(self,folder='outputs'):
    FileWriter.__init__(self,'id_dsa','key',folder)
  def writeToFile(self,instance):
    prefix=self.prefix
    filename=self.get_valid_filename()
    f=libc.fopen(filename,"w")
    ret=_libssl.PEM_write_DSAPrivateKey(f, ctypes.byref(instance), None, None, 0, None, None)
    if ret < 1:
      log.error("Error saving key to file %s"% filename)
      return False
    log.info ("[X] Key saved to file %s"%filename)
    return True
  

class OpenSSLStructFinder(StructFinder):
  ''' Must not fork to ptrace. We need the real ctypes structs '''
  # interesting structs
  rsaw=RSAFileWriter()
  dsaw=DSAFileWriter()  
  def __init__(self, mappings, targetmapping):
    StructFinder.__init__(self, mappings, targetmapping)
    self.OPENSSL_STRUCTS={     # name, ( struct, callback)
      'RSA': (ctypes_openssl.RSA, self.rsaw.writeToFile ),
      'DSA': (ctypes_openssl.DSA, self.dsaw.writeToFile )
      }
  def findAndSave(self, maxNum=1, fullScan=False, nommap=False):
    log.debug('look for RSA keys')
    outs=self.find_struct(ctypes_openssl.RSA, maxNum=maxNum )
    for rsa,addr in outs:
      self.save(rsa)    
    log.debug('look for DSA keys')
    outs=self.find_struct(ctypes_openssl.DSA, maxNum=maxNum)
    for dsa,addr in outs:
      self.save(dsa)    
    return
  #'BIGNUM':   'RSA': (ctypes_openssl.BIGNUM, )
  def save(self,instance):
    if type(instance) == ctypes_openssl.RSA:
      self.rsaw.writeToFile(instance)
    elif type(instance) == ctypes_openssl.DSA:
      self.dsaw.writeToFile(instance)
    else:
      log.error('I dont know how to save that : %s'%(instance))

def usage(txt):
  log.error("Usage : %s <pid> [offset] # find SSL Structs in process"% txt)
  sys.exit(-1)


def argparser():
  parser = argparse.ArgumentParser(prog='openssl.py', description='Capture of RSA and DSA keys.')
  parser.add_argument('pid', type=int, help='Target PID')
  parser.add_argument('--nommap', dest='mmap', action='store_const', const=False, default=True, help='disable mmap()-ing')
  parser.add_argument('--debug', dest='debug', action='store_const', const=True, help='setLevel to DEBUG')
  parser.set_defaults(func=search)
  return parser


def search(args):
  if args.debug:
    logging.basicConfig(level=logging.DEBUG)    
  log.info("Target has pid %d"%args.pid)
  mappings = MemoryMapper(args).getMappings()
  targetMapping = [m for m in mappings if m.pathname == '[heap]']
  if len(targetMapping) == 0:
    log.warning('No [heap] memorymapping found. Searching everywhere.')
    targetMapping = mappings
  finder = OpenSSLStructFinder(mappings, targetMapping)
  outs=finder.findAndSave()
  return


def main(argv):
  logging.basicConfig(level=logging.INFO)

  # use optarg on v, a and to
  parser = argparser()
  opts = parser.parse_args(argv)
  try:
    opts.func(opts)
  except ImportError,e:
    log.error('Struct type does not exists.')
    print e

        
  log.info("done for pid %d"%opts.pid)

  return -1


if __name__ == "__main__":
  main(sys.argv[1:])

