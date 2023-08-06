#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Loic Jaquemet loic.jaquemet+python@gmail.com
#

__author__ = "Loic Jaquemet loic.jaquemet+python@gmail.com"

import logging,os,socket,select, sys,threading, time

import scapy.config

from lrucache import LRUCache
from ctypes_openssh import AES_BLOCK_SIZE

log=logging.getLogger('socket.scapy')

WAIT_RETRANSMIT=5
MISSING_DATA_MESSAGE='[MISSINGDATA456]'

def isdestport22(packet):
  return  packet.dport == 22

def isNotdestport22(packet):
  return  not isdestport22(packet)


def hexify(data):
  s=''
  for i in range(0,len(data)):
    s+="%02x"% ord(data[i])
    if i%16==15:
      s+="\r\n"
    elif i%2==1:
      s+=" "
  #s+="\r\n"
  return s


class MissingDataException (Exception):
  def __init__(self,nb):
    self.nb=nb
 
class state:
  name=None
  packet_count=0
  byte_count=0
  start_seq=None
  max_seq=0
  expected_seq=0
  queue=None
  write_socket=None
  read_socket=None
  read_socket_revc_func=None
  ts_missing=None
  def __init__(self,name):
    self.name=name
    self.queue={}
  def init(self, pair):
    read, write = pair
    self.read_socket=socket.socket(_sock=read)
    self.read_socket_revc_func=self.read_socket.recv
    #self.read_socket.recv = self._wrapped_recv # will be used to lock-wrap
    self.write_socket=write
    return  

  def enqueue(self, packet):
    self.queue[packet.seq]= packet
    return
    

  def forget_missing_data(self):
    ''' switch recv() method on readsocket to alert reader()
     push missing data in socket to wakeup reader
    '''
    if self.ts_missing is None: # naaa. it's good
      return
    self.ts_missing=None
    #
    if self.read_socket.recv != self._read_missing_data:
      log.warning('socket empty... we switch to Missing mode => send(MISSING_DATA_MESSAGE)')
      self.read_socket.recv = self._read_missing_data
    return
    
  def _read_missing_data(self, n):
    ''' exception contains lenght of missing data '''
    # repair socket for further use
    self.read_socket.recv = self.read_socket_revc_func
    #self.read_socket.recv = self._wrapped_recv    
    nb = self.expected_seq - self.max_seq
    new_seq = min(self.queue.keys())
    nbreal = new_seq - self.max_seq
    log.debug('%s: Forgetting about r:%d e:%d bytes / %d pkts left, expected: %d, new_seq: %d'%(
                            self.name, nbreal, nb, len(self.queue), self.expected_seq ,new_seq ))
    raise MissingDataException(nbreal)
  
  def __str__(self):
    return "%s: %d bytes/%d packets max_seq:%d expected_seq:%d q:%d"%(self.name, self.byte_count,self.packet_count,
                self.max_seq,self.expected_seq, len(self.queue))
  
class stack:
  def __init__(self):
    self.inbound=state('inbound')
    self.outbound=state('outbound')
  def __str__(self):
    return "\n%s\n%s"%(self.inbound,self.outbound)
  
class socket_scapy():
  ''' what you write in writeso, gets read in readso '''
  worker=None
  def __init__(self,filterRules, protocolName='TCP', packetCount=0, timeout=None,
            isInboundPacketCallback=None,isOutboundPacketCallback=None):
    ''' 
    @param filterRules: a pcap compatible filter string 
    @param protocolName: the name of the scapy proto layer 
    @param packetCount: 0/Unlimited or packet capture limit
    @param timeout: None/Unlimited or stop after
    '''
    # set scapy to use native pcap instead of SOCK_RAW
    scapy.config.conf.use_pcap=True

    self._cache_seqn = LRUCache(128)
    ## if using SOCK_RAW, we need to mess with filter to up the capture size higher than 1514/1600 bytes
    #maxSize="\' -s \'0xffff" # abusing scapy-to-tcpdump string format 
    #self.filterRules=filterRules + maxSize
    self.filterRules=filterRules
    self.protocolName=protocolName
    self.packetCount=packetCount
    self.timeout=timeout
    #
    self.lock=threading.Lock()
    self.stack=stack()
    self.packets={}
    self.bigqueue=[]

    self._running_thread=None
    # distinguish between incoming and outgoing packets // classic ssh client
    self.__is_inboundPacket=isInboundPacketCallback
    self.__is_outboundPacket=isOutboundPacketCallback
    if ( self.__is_inboundPacket is None):
      self.__is_inboundPacket=isNotdestport22 ## SSH CLIENT
      ##self.__is_inboundPacket=isdestport22  ## SSH SERVER
    if ( self.__is_outboundPacket is None):
      self.__is_outboundPacket=isdestport22  ## SSH CLIENT
      ##self.__is_outboundPacket=isNotdestport22 ## SSH SERVER
    # make socket
    try:
        isWindows = socket.AF_UNIX
        self.stack.inbound.init(  socket.socketpair() )
        self.stack.outbound.init( socket.socketpair() )
    except NameError:
        # yes || no socketpair support anyway
        self._initPipes()
    # scapy config
    # loopback
    #log.info('MTU is %d'%(scapy.data.MTU ))
    #scapy.data.MTU=0x7fff
    return
  
  def _initPipes(self):
    self.stack.inbound.pipe  = pipe_socketpair()
    self.stack.inbound.init(  self.stack.inbound.pipe.socketpair())
    self.stack.outbound.pipe = pipe_socketpair()
    self.stack.outbound.init( self.stack.outbound.pipe.socketpair() )
    return

  def getInboundSocket(self):
    return self.stack.inbound.read_socket
  def getOutboundSocket(self):
    return self.stack.outbound.read_socket

  def run(self):
    # scapy - with config initialised
    #scapy.sendrecv.sniff(count=self.packetCount,timeout=self.timeout,store=0,filter=self.filterRules,prn=self.cbSSHPacket)
    from scapy.all import sniff
    log.info('Using L2listen = %s'%(scapy.config.conf.L2listen)) 
    # XXX TODO, define iface from saddr and daddr // scapy.all.read_routes()
    sniff(count=self.packetCount, timeout=self.timeout, store=0, filter=self.filterRules, prn=self.enqueue, iface='any')
    log.warning('============ SNIFF Terminated ====================')
    return

  def enqueue(self, obj):
    self.lock.acquire()
    self.bigqueue.append(obj)
    self.lock.release()
    return
  def dequeue(self):
    obj=None
    self.lock.acquire()
    if len(self.bigqueue) > 0:
      obj=self.bigqueue.pop(0)
    self.lock.release()
    return obj

  def prequeue(self, state):
    ''' get packets from queue and put them in processing bigqueue '''
    queue=state.queue.values()
    queue.sort(key=lambda p: p.seq)
    # add the first and the next that are in perfect suite.
    toadd=[queue.pop(0),]
    for i in xrange(0,len(queue)):
      if toadd[-1].seq+len(toadd[-1].payload) == queue[0].seq :
        toadd.append(queue.pop(0))
      else:
        log.debug('Stop prequeuing  toadd[-1].seq+len(toadd[-1].payload): %d , queue[0].seq: %d'%(toadd[-1].seq+len(toadd[-1].payload) , queue[0].seq ))
        break
    # let remaining in state.queue
    state.queue=dict( [ (p.seq, p) for p in queue])
    self.lock.acquire()
    #preprend packets
    self.bigqueue = toadd + self.bigqueue
    self.lock.release()
    log.debug('Prequeued %d packets, remaining %d, queued from %d to %d '%(
                        len(toadd), len(state.queue), toadd[0].seq, (toadd[-1].seq + len(toadd[-1].payload)) 
                        ))
    # reset time counter
    if len(state.queue) > 0:
      state.ts_missing  = time.time()
    else:
      state.ts_missing  = None
    return
  
  def run2(self):
    while(True):
      # depile packets
      packet=self.dequeue()
      self.cbSSHPacket(packet)
      if packet is None:
        if time.time() %10 == 0:
          log.debug('%s'%(self))
        time.sleep(0.5)
    log.warning('============ SNIFF WORKER Terminated ====================')
    return
    
  def checkState(self,state, packet):
    seq=packet.seq    
    ## debug head initialisation
    if state.start_seq is None:
      state.start_seq=seq
      state.expected_seq=seq
    ## we should not processs empty packets
    payloadLen=len(packet.payload)
    if payloadLen == 0:
      return False

    # packet is expected 
    if seq == state.expected_seq: # JIT
      state.max_seq = seq
      state.expected_seq = seq + payloadLen
      self.packets[seq]=packet # debug the packets
      state.ts_missing = None
      # check if next is already in state.queue , if expected has changed
      if state.expected_seq in state.queue : 
        log.debug('in state.queue: seqnum %d len: %d %s'%(seq, payloadLen, state ))
        log.debug('we have next ones in buffer %d'%(state.expected_seq)) # prepend the queue to parse list.
        self.prequeue(state)
      return True

    # packet is future
    elif seq > state.expected_seq: # future anterieur
      # seq is in advance
      state.enqueue(packet)
      #log.debug('Queuing packet seq: %d len: %d %s'%(seq, payloadLen, state))
      ## if ~5 sec, we will forget about missing data
      ## and inform reader of that fact
      if state.ts_missing is None:
        state.ts_missing = time.time()
      elif time.time() > ( state.ts_missing + WAIT_RETRANSMIT) : # waiting for too long
        state.forget_missing_data()
      else:
        pass
      # check if next is already in state.queue 
      if state.expected_seq in state.queue :
        log.debug('queuing, seqnum %d len: %d %s'%(seq, payloadLen, state ))
        log.debug('queuing, we have next ones in buffer %d'%(state.expected_seq)) # prepend the queue to parse list.
        self.prequeue(state)
        # reset time counter
        state.ts_missing  = None
      else:
        ## if ~5 sec, we will forget about missing data
        ## and inform reader of that fact
        if state.ts_missing is None:
          state.ts_missing = time.time()
        elif time.time() > ( state.ts_missing + WAIT_RETRANSMIT) : # waiting for too long
          state.forget_missing_data()
        else:
          pass
      #do not parse this one 
      return False

    # packet is a retranmission 
    elif seq < state.expected_seq:
      # TCP retransmission
      log.debug('TCP retransmit - We just received %d when we already processed %d'%(seq, state.max_seq))
      # never hitted
      if seq+payloadLen > state.expected_seq :
        log.warning(' ***** EXTRA DATA FOUND ON TCP RETRANSMISSION ')
        # we need to recover the extra data to put it in the stream
        nb=(seq+payloadLen) - state.expected_seq
        data=packet.payload.load[-nb:]
        log.warning('packet seq %d has already been received'%(seq))
        log.warning('recent  packet : %s'%(repr(packet.underlayer) ))
        log.warning('first   packet : %s'%(repr(self.packets[seq].underlayer ) ))
        seq2=seq+len(self.packets[seq].payload)
        log.warning('first+1 packet : %s'%(repr(self.packets[seq2].underlayer ) ))
        packet.payload.load=data
        log.warning('NEW     packet : %s'%(repr(packet.underlayer) ))
        # updates seq
        state.max_seq = seq
        state.expected_seq = seq2
        # save it
        self.packets[seq]=packet # debug the packets
        # we can process this one
        return True
      # ignore it
      return False
    # else, seq < expected_seq and seq >= state.max_seq. That's not possible... it's current packet.
    # it's a dup already dedupped ? partial fragment ?
    log.warning('received a bogus fragment seq: %d for %s'%(seq, self))
    return True

  def cbSSHPacket(self, obj):
    ''' callback function to pile packets in socket'''
    # check queues only
    if obj is None:
      for state in [self.stack.inbound,self.stack.outbound]:
        if state.expected_seq in state.queue : 
          self.prequeue(state)
        if state.ts_missing is not None and  time.time() > ( state.ts_missing + WAIT_RETRANSMIT) : # waiting for too long
            state.forget_missing_data()
      return None
    # triage
    packet=obj[self.protocolName]
    pLen=len(packet.payload)
    if pLen == 0: # ignore acks and stuff 
      return None
    # real triage
    if self.__is_inboundPacket(packet):
      if self.checkState(self.stack.inbound, packet) and pLen > 0:
        self.writePacket(self.stack.inbound, packet.payload.load )
    elif self.__is_outboundPacket(packet):
      if self.checkState(self.stack.outbound, packet) and pLen > 0:
        self.writePacket(self.stack.outbound, packet.payload.load )
    else:
      log.error('the packet is neither inbound nor outbound. You messed up your filter and callbacks.')
    return None
    
  def setThread(self,thread):
    ''' the thread using the pipes '''
    self._running_thread=thread
    return 
  
  def writePacket(self,state, payload):
    #if state.name == 'inbound':
    #  log.debug("writePacket%s %d + len: %d = %d"%(state.name, state.byte_count, len(payload), state.byte_count+ len(payload) ) )

    state.byte_count+=self.addPacket(payload,state)
    state.packet_count+=1
    #log.debug("writePacket%s %d len: %d\n%s"%(state.name, state.byte_count, len(payload), hexify(payload) ) )
    return 
    
  def addPacket(self,payload, state):
    cnt=state.write_socket.send(payload)
    #log.debug("buffered %d/%d bytes"%(cnt, len(payload) ) )
    return cnt
  
  def __str__(self):
    return "<socket_scapy %s "%(self.stack) 

# if Linux use socket.socketpair()
class pipe_socketpair(object):
  def __init__(self):
    self.readfd,self.writefd=os.pipe()
    self.readso=socket.fromfd(self.readfd,socket.AF_UNIX,socket.SOCK_STREAM)
    self.writeso=socket.fromfd(self.writefd,socket.AF_UNIX,socket.SOCK_STREAM)
    return
  def socketpair(self):
    return (self.readso,self.writeso)

def test():
  '''
sniff(count=0, store=1, offline=None, prn=None, lfilter=None, L2socket=None, timeout=None, opened_socket=None, *arg, **karg)  
  '''
  port=22
  sshfilter="tcp and port %d"%(port)
  soscapy=socket_scapy(sshfilter,packetCount=10)
  log.info('Please make some ssh  traffic')
  soscapy.run()
  print 'sniff finished'
  # we get Ether()'s...
  print soscapy.stats()
  l=soscapy._inbound_cnt
  print 'trying to read'
  data=soscapy.getInboundSocket().recv(l)
  print 'recv %d bytes ->',len(data),repr(data)
  return soscapy

#test()

