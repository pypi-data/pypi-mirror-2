import re
import binascii
from urllib.request import urlopen
from bitstring import BitString

def encode(s):
  return binascii.hexlify(s).decode('ascii')

def decode(s):
  return binascii.unhexlify(s.encode('ascii'))

def encodeAddress(addr):
  ip=addr[0]
  if ip=='':
    ip='::'
  port=addr[1]
  if '.' in ip:
    return ip+':'+str(port)
  else:
    return '['+ip+']:'+str(port)

def decodeAddress(s):
  if '.' in s:
    parts=s.split(':')
    return (parts[0], int(parts[1]), False)
  else:
    m=re.match('\[([0-9a-f:]+)\]:([0-9]+)', s)
    return (m.group(1), int(m.group(2)), True)

def getPublicIP(v6=True):
  if v6:
    text=urlopen("http://ipv6.ip6.me/").read()
    match=re.search(b"\+3>([^<]+)<", text)
#    ip=urlopen("http://whatismyv6ip.com/myip").read()
#    return ip.decode('ascii')
    ip=match.group(1)
    return ip.decode('ascii')
  else:
    text=urlopen("http://ip4.me/").read()
    match=re.search(b"\+3>([^<]+)<", text)
#    ip=urlopen("http://whatismyv6ip.com/myip").read()
#    return ip.decode('ascii')
    ip=match.group(1)
    return ip.decode('ascii')

def getAddress(port):
  return encodeAddress((getPublicIP(), port))

def splitFields(msg, fields):
  try:
    values=[]
    for field in fields:
      value=msg[:field]
      msg=msg[field:]
      values.append(value)
    if len(msg)>0:
      values.append(msg)
    return values
  except:
    return None

def splitField(msg, field):
  return msg[:field], msg[field:]

def decodeFlags(flagsByte):
  bits=BitString(bytes=flagsByte)
  bools=[]
  for x in range(bits.length):
    bools.append(bits.readbit().uint==1)
  return bools

def encodeFlags(bools):
  bits=BitString()
  for bool in bools:
    if bool:
      bits.append(BitString('0b1'))
    else:
      bits.append(BitString('0b0'))
  return bits.bytes

def fill(bytes, size):
  while len(bytes)<size:
    bytes=bytes+b'\x00'
  return bytes

def xor(a, b):
  if len(a)!=len(b):
    print('xor parameters must be the same length:', len(a), len(b))
    return None
  c=bytearray()
  for x in range(len(a)):
    c.append(a[x] ^ b[x])
  return bytes(c)
