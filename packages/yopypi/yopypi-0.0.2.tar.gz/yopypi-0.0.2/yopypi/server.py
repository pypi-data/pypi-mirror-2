from os import path

from bottle import debug, redirect, route, run
from status import running

from yopypi import logging, config_defaults


# Fixes a call from a different path
CWD = path.abspath(__file__)
APP_CWD = path.dirname(CWD)

# Initialize config
config = config_defaults()
log = logging(module='server')


@route('/:uri#(.*)$#')
def index(uri):
    up = running()
    if up:
        log.write("pypi is up, redirecting to http://pypi.python.org/%s" % uri)
        redirect('http://pypi.python.org/%s' % uri)
    else:
         log.write("pypi seems to be down, trying mirrors")
         for mirror in config['mirrors']:
             up = running(host=mirror)
             if up:
                 redirect(mirror+uri)
                 log.write("mirror %s is up, redirecting..." % mirror)
             else:
                 log.write("mirror %s is down, trying next one..." % mirror)

def main():
    try:
        log.write("running yopypi server...")
        debug(True)
        run(host=config['web_host'], port=config['web_port'], quiet=True)
    except Exception, e:
        log.write("Couldn't start the yopypi server:%s" % e)


if __name__ == '__main__':
    main()
