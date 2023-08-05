import sys
import time
import struct
from socket import *

import yaml

from dust.crypto.curve import *
from dust.extensions.onion.onion_packet import OnionPacket
from dust.core.util import encodeAddress, encode
from dust.intro.intro import Introducer

class onion_socket:
  def __init__(self, keys, socket):
    self.keys=keys
    self.keypair=keys.getKeypair()
    self.sock=socket

    self.sessionKeys={}

    self.remaining=None

  def recvfrom(self, bufsize):
    if self.remaining:
      data, addr, endpoint=self.remaining
      self.remaining=None
    else:
      data, addr, endpoint=self.sock.recvfrom(bufsize)

    if not data:
      print('Onion: No data')
      return None, None, None
    else:
      packet=self.decodeOnionPacket(data)
      if not packet:
        print('Onion: No packet')
        return None, None, None
      else:
        #print('Packet:')
        #print(packet)
        if packet.remaining:
          self.remaining=(packet.remaining, addr, packet.endpoint)
        if type(packet)==OnionPacket:
          return packet.data, addr, packet.endpoint
        else:
          print('Not a data packet')
          return None, None, None

  def sendto(self, data, addr, endpoint):
    print('sendto '+str(endpoint))
    packet=self.encodePacket(endpoint, data)
    print('Sending')
    print(packet)
    self.sock.sendto(packet.packet, 0, addr)

  def decodePacket(self, endpoint, data):
    packet=OnionPacket()
    packet.decodeOnionPacket(data)
    if packet.checkMac() and packet.checkTimestamp():
      return packet
    else:
      print('Integrity failed', packet.checkMac(), packet.checkTimestamp())
      print(packet)
      return None
    else: # Must be an intro packet
      print('Unknown address', endpoint)
      if self.introducer:
        intro=self.introducer.acceptIntroduction(data, endpoint)
        if intro:
          return intro
        else:
          return None

  def encodePacket(self, endpoint, data):
    packet=OnionPacket()
    packet.createOnionPacket(self.keys.getKeypair(), endpoint, data, self.keys.entropy)
    return packet

