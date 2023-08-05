from sys import argv
from os import path, environ, mkdir

from yopypi import server, logging, config_options, config_defaults
from supay import Daemon


# Fixes a call from a different path
CWD = path.abspath(__file__)
APP_CWD = path.dirname(CWD)

# local pid dir to avoid running as root
PID_DIR = APP_CWD

user_dir = environ.get('HOME')
yopypi_dir = user_dir+'/.yopypi'
log = logging(module='cli')

def local_env_init():
    "Make sure we have a local dir to put some log files"
    if path.isdir(yopypi_dir):
        pass
    else:
        mkdir(yopypi_dir)

def start(config=config_defaults()):
    log.write('starting server from cli')
    daemon = Daemon(
            name='yopypi', 
            pid_dir=PID_DIR, 
            stdin=yopypi_dir,
            stdout=yopypi_dir,
            stderr=yopypi_dir
            )
    daemon.start()
    try:
        server.config = config
        server.main()
    except Exception, e:
        log.write(e)

def stop():
    log.write('shutting down server from cli')
    daemon = Daemon('yopypi', pid_dir=PID_DIR)
    daemon.stop()

def main():
    if len(argv) >= 2:
        local_env_init()
        if argv[1] == 'start':
            try:
                config = config_options(argv[2])
                start(config)
            except IndexError:
                start()
        if argv[1] == 'stop':
            stop()
    else:
        print 'Usage: \nyopypi [start|stop] [configuration file]\n'
