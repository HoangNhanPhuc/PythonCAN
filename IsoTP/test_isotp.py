import isotp

s = isotp.socket()
s2 = isotp.socket()
# Configuring the sockets.
s.set_fc_opts(stmin=5, bs=10)
#s.set_general_opts(...)
#s.set_ll_opts(...)

s.bind("vcan0", isotp.Address(rxid=0x123, txid=0x456))
s2.bind("vcan0", isotp.Address(rxid=0x456, txid=0x123))
s2.send(b"Hello, this is a long payload sent in small chunks of 8 bytes.")
print(s.recv())