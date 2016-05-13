import socket
import sys

argLength = len(sys.argv)
data = bytearray(argLength-3)

# build the operator
if sys.argv[3] == '+':
  data[0] = 1
elif sys.argv[3] == '-':
  data[0] = 2
elif sys.argv[3] == '*':
  data[0] = 4

# get the arg count
data[1] = argLength - 4

# pad the byte array
i = 4
j = 2
while i < argLength:
  if i % 2 == 0:
    a = int(sys.argv[i])
    x = a << 4
    if i+1 != argLength:
      b = int(sys.argv[i+1])
      x = x | b
    else:
      x = a << 4
    data[j] = x
    i += 2
    j += 1

# connect and send byte array to the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((sys.argv[1], int(sys.argv[2])))
s.sendall(data)

# recieve data
result = bytearray(4)
s.recv_into(result)
s.close()

# unpack data
i = 0
k = len(result)*8-8
answer = 0
mask = 0b11110000
mask2 = 0b00001111
while i < len(result):
  a = result[i]
  answer += a << k
  i += 1
  k -= 8

# check for negative
if answer >= 2**31:
  answer -= 2**32

print(answer)
