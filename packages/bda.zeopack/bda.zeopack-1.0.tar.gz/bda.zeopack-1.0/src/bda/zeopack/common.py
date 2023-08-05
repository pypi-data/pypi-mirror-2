import logging
logger = logging.getLogger('bda.zeopack')

from ZEO.ClientStorage import ClientStorage

def pack(host, port, storage, days=0):
    zeoclient = ClientStorage([(host, int(port))], storage=storage, wait=1, 
                              read_only=1)
    zeoclient.pack(wait=1, days=days)
    zeoclient.close()
    
def packmultiple(cfg):
    """packs multiple storages on one or different servers

    expects a list with dicts like:
    
    >>> cfg = [{
    ...     'server': 'dummy.zoplo.com:8100',
    ...     'storages': ['root01', 'mount01', 'mount02'],
    ...     'days': 1,
    ...     }]
    """
    for item in cfg:
        host, port = item['server'].split(':')
        for storage in item['storages']:
            logger.info("packing ZODB storage %s on %s:%s (days=%s) " % \
                       ( storage, host, port, item['days']))
            pack(host, port, storage, item['days'])