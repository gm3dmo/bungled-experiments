import asyncore, socket
 
"""
The purpose of this script is to allow you to check that your
application is sending out SNMP traps.  This should run in the
python2/3. It might run in jython but even if it did you don't have
root on a Solaris box so you are out of luck for Solaris. If you want to run it on the default port for SNMP (162) then you will need root privilege to bind to that.
 Note that this isn't an SNMP daemon, it doesn't know how to parse the
snmp information it receives it just blindly prints it to the screen so that you can confirm the sendind party/app is raising the traps.
 
 
$ sudo su -
# python snmp_listener.py
 
"""

bind_address = '0.0.0.0'
listen_port = 10062
 
class AsyncoreServerUDP(asyncore.dispatcher):
   def __init__(self):
      asyncore.dispatcher.__init__(self)
 
      # Bind to port 162 on all interfaces
      self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.bind((bind_address, listen_port))
 
   # Even though UDP is connectionless this is called when it binds to a port
   def handle_connect(self):
      print("Server Started...")
 
   # This is called everytime there is something to read
   def handle_read(self):
      data, addr = self.recvfrom(2048)
      print(str(addr)+" >> "+data)
      print("===========================")
 
   # This is called all the time and causes errors if you leave it out.
   def handle_write(self):
      pass

 
AsyncoreServerUDP()
asyncore.loop()
