import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(sys.argv[1])
s.bind(('', port))

while True:
  data = bytearray(7)
  nBytes, address = s.recvfrom_into(data)
  i = 2
  result = 0

  # unpack the nibbles
  while i < nBytes:
    x = data[i]
    MASK_HIGH = 0b11110000
    MASK_LOW = 0b00001111
    a = (x & MASK_HIGH) >> 4
    b = (x & MASK_LOW)

    # calculate
    if data[0] == 1:
      result = result + a + b
    elif data[0] == 2:
      if i == 2:
        result = a
        result -= b
      else:
        result = result - a - b
    else:
      if i == 2:
        result = a
        result *= b
      elif i == nBytes - 1 and i % 2 != 0:
        result *= a 
      else:
        result = result * a * b
    i += 1

  # create masks and pack number
  MASK_MSB = 0b11111111000000000000000000000000
  MASK_MIDLEFT = 0b00000000111111110000000000000000
  MASK_MIDRIGHT = 0b00000000000000001111111100000000
  MASK_LSB = 0b00000000000000000000000011111111

  data[0] = (result & MASK_MSB) >> 24
  data[1] = (result & MASK_MIDLEFT) >> 16
  data[2] = (result & MASK_MIDRIGHT) >> 8
  data[3] = (result & MASK_LSB)

  #return result
  s.sendto(data, address)
