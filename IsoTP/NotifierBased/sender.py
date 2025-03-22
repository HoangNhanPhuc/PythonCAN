# In this example, we transmit a payload using a blocking send()
import isotp
import logging

from can.interfaces.socketcan import SocketcanBus

def my_error_handler(error):
    # Called from a different thread, needs to be thread safe
    logging.warning('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))

bus = SocketcanBus(channel='vcan0')
addr = isotp.Address(isotp.AddressingMode.Normal_11bits, rxid=0x123, txid=0x456)
params = {
    'blocking_send' : True
}
stack = isotp.CanStack(bus, address=addr, error_handler=my_error_handler, params=params)

try:
    stack.start()
    stack.send(b'Hello, this is a long payload sent in small chunks',send_timeout=2)    # Blocking send, raise on error
    print("Payload transmission successfully completed.")     # Success is guaranteed because send() can raise
except isotp.BlockingSendFailure:   # Happens for any kind of failure, including timeouts
    print("Send failed")
finally:
    stack.stop()
    bus.shutdown()