from pykka.actor import Actor
from pykka.future import Future, get_all, wait_all
from pykka.proxy import ActorProxy, CallableProxy
from pykka.registry import ActorRegistry


__all__ = ['Actor', 'ActorProxy', 'ActorRegistry', 'CallableProxy', 'Future',
    'get_all', 'wait_all']


VERSION = (0, 5)

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if len(VERSION) > 2:
        version = '%s.%s' % (version, VERSION[2])
    return version
