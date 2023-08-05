import sys
import logging
from ConfigParser import ConfigParser
from bda.zeopack.common import packmultiple
from bda.zeopack.common import logger

DEFAULTFILE = '/etc/zeopack.cfg'

logging.basicConfig()
logger.setLevel(logging.INFO)

def zhelp(msg=None):
    if msg is not None:
        print '\n', msg, '\n'
    print "Usage: zeomultipack [config-file]"
    print "Default config file is expected at %s" % DEFAULTFILE
    print "File-Format example:"
    print "[192.168.1.1:8100]"
    print "days = 1"
    print "storages ="
    print "    storage01"
    print "    storage02"
    print ""
    print "[192.168.1.2:8100]"
    print "days = 1"
    print "storages ="
    print "    storage02"
    print "..."
    raise SystemExit()

def _parse(filename):
    try:
        cfgfile = open(filename, 'r')
    except:        
        zhelp('ERROR: config-file %s not found!' % filename)
    logger.info('Use configuration at %s' % filename)
    config = ConfigParser()
    config.readfp(cfgfile)
    zpcfg = []
    for section in config.sections():
        part = dict()
        part['server'] = section
        part['days'] = int(config.get(section, 'days'))
        part['storages'] = config.get(section, 'storages').split()
        zpcfg.append(part)
    return zpcfg    

def main():
    print "zeomultipack - pack multiple Zope Databases at one or more " + \
          "ZEO servers."
    filename = DEFAULTFILE
    if len(sys.argv) > 1:
        filename = sys.argv[1] 
        if '--help' in filename:
            zhelp()
            exit()            
    zpcfg = _parse(filename)            
    packmultiple(zpcfg)
    
if __name__ == '__main__':
    main()    