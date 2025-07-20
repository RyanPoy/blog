---
title: Python Socket Programming
date: 2010-06-13

category: Tech
tags: [Python, Socket]
---

## synchronization

### TCP

server:
```python
server = socket(AF_INET, SOCK_STREAM)
server.bind((ip, port))
server.listen(5)
new_sock, address = server.accept()
new_sock.send(...)
new_sock.recv(...)
new_sock.close()
```

client:
```python
client = socket(AF_INET, SOCK_STREAM)
client.connect(ip, port)
client.send(...)
client.recv(...)
client.close()
```

### UDP

server:
```python
server = socket(AF_INET, SOCK_DGRAM)
server.bind((ip, port))
data, address = server.recvfrom(...)
server.sendto(data, address)
```

client:
```python
client = socket(AF_INET, SOCK_DGRAM)
client.recvfrom()
client.sendto(data, address)
```


## asynchronization

server:
```python
class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(AF_INET, SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

        def handle_accept(self):
            pair = self.accept()
            if pair is not None:
                sock, address = pair[0], pair[1]
                server_handler(sock, address)

class ServerHandler(asyncore.dispatcher):
            
    def __init__(self, sock, address):
        asyncore.dispatcher.__init__(sock)
                
    def handle_write(self):
        pass

    def handle_read(self):
        pass

    def readable(self):
        pass
            
    def writable(self):
        pass

    def handle_close(self):
        pass
```

client：
```python
class Client(asyncore.dispatcher):
                
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.connect((host, port))

    def handle_write(self):
        pass

    def handle_read(self):
        pass

    def readable(self):
        pass

    def writable(self):
        pass

    def handle_close(self):
        pass
```
