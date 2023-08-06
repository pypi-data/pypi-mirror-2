This is srplib based on SRPSocket version 1.1 found at 
http://members.tripod.com/professor_tom/archives/srpsocket.html
original file is in contrib directory.


srplib is a Python module that implement basic SRP authentication protocol.


sock module provide a synchronous version of the socket library
asyn module provide a asynchronous version of the asynchat library

A simple "echo" server and client is provided as sample. Both samples can be
mixed together. 

This code is released under the GNU GENERAL PUBLIC LICENSE
Be careful to fulfil the requirements of the use of the SRP authentication system.   


usage sample:
=============


Create and edit password file
 

$ python srplib.py passwd 
srpdb> help

Undocumented commands:
======================
EOF  del  exit  help  list  passwd  quit  save
srpdb> list
['user.asx', 'client.new', 'user.toto', 'user.new', 'user.manager', 'client.web232', 'mary']
srpdb> passwd foo
Enter new password for foo: 
srpdb> list
['user.asx', 'client.new', 'user.toto', 'user.new', 'user.manager', 'client.web232', 'foo', 'mary']


The asyn client and server samples:
====================================
$ python asyn.py -h
Usage: asyn.py [options]

Options:
  -h, --help            show this help message and exit
  -s, --server          start the server
  -c, --console         start the client
  -p port, --port=port  the port
  -d filename, --database=filename
                        the user database filename
  -u username, --user=username
                        the username
  -a password, --password=password
                        the user password

start the asyn server

$ python asyn.py -s -d passwd
echo server started
new incoming connection from ('127.0.0.1', 46756)
session opened for user "mary"
received : 'hello world'
received : 'exit'

start the asyn client

$ python asyn.py -c -u mary -a poppins
connected as mary
hello world
bye

 
The socket based client and server samples:
============================================
$ python sock.py -h
Usage: sock.py [options]

Options:
  -h, --help            show this help message and exit
  -s, --server          start the server
  -c, --console         start the client
  -p port, --port=port  the port
  -d filename, --database=filename
                        the user database filename
  -u username, --user=username
                        the username
  -a password, --password=password
                        the user password
                        
start the server 

$ python sock.py -s -d password
echo server started
session opened for user "mary"
received : 'hello world\r\n'
received : 'exit\r\n'

start the client 

$ python sock.py -c -u mary -a poppins
Logged in
hello world
exit
bye



== This is the original README file from SRPSocket.tgz in contrib directory ==

This is SRPSocket version 1.1

SRPSocket is a Python module that creates an _authenticated_ socket.  The
socket is authenticated using the SRP (Secure Remote Password) protocol.
SRP is safe to use over the network.  It resists offline dictionary attacks,
man-in-the-middle attacks, allows both client and host authentication (to
prevent host spoofing), creates a secure, shared session key as a side
effect, and has several other nice properties.

Note that the term 'password' may safely and usefully be replaced with the
term 'passphrase', as the latter are usually more secure (i.e.  have more
bits of entropy) and easier to remember.

The home page for SRP is http://srp.stanford.edu/.

This version uses SHA hashes.  If your version of Python does not have SHA
hashes, consider upgrading to the latest version of Python, or simply
replace all references to "sha" with "md5".

SRP uses arithmetic in a prime field.  The distribution comes with one
preselected safe prime that is about 120 bits long.  Feel free to use
others, but keep in mind that the client and the server must agree on the
set of primes used.

To begin, create the passwd database with "python SRP.py" (see client.py).
In this version, the passwd file is just in the local directory of the
server, and no mode setting is done.  The passwd file should not be world
readable, since that allows offline dictionary attacks.  Note again that
even if it is readable (like the standard /etc/passwd), use of long pass
phrases instead of passwords can help tremendously.

Finally, remember that many breaches of security involve buggy servers, such
as those susceptible to buffer overflow exploits that totally bypass any
passphrase, secure or not.  But SRP will at least stop you from sending
passwords over the net in the clear!

Dr. Tom
tomh@po.crl.go.jp
