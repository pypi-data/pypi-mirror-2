import socket
from yopypi import logging


log = logging(module='status')

def running(host='pypi.python.org', port=80):
    socket.setdefaulttimeout(0.8)
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send('X')
        s.close()
        log.write("verified PYPI server status at port 80")
        return True
    except Exception, e:
        log.write("Could not connect to %s at port %d  %s" % (host, port, e))
        return False

if __name__ == "__main__":
        running()
