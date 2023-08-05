import datetime
import re
import socket

import memcache


__all__ = ('MemcacheInspector', 'MemcacheItem', 'MemcacheInspectorError', 'get_items')
__version_info__ = (0, 2, 0)
__version__ = '.'.join([str(x) for x in __version_info__])


class MemcacheInspectorError(Exception):
    pass


class MemcacheItem:
    def __init__(self, key, size, expiration, value=None):
        self.value = value
        if not key:
            raise MemcacheInspectorError('A key must be specified.')
        else:
            self.key = str(key)

        try:
            self.size = int(float(size))
            assert self.size >= 0
        except:
            raise MemcacheInspectorError('A valid size (in bytes) must be specified.')

        if isinstance(expiration, datetime.datetime):
            self.expiration = expiration
        else:
            try:
                self.expiration = datetime.datetime.fromtimestamp(float(expiration))
            except:
                raise MemcacheInspectorError('A valid date must be specified.')

    def __str__(self):
        return '%s (%sb)' % (self.key, self.size)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, str(self))

    def equals(self, other, ignore_expiration=False):
        test =  self.key == other.key \
                and self.size == other.size \
                and self.value == other.value

        if not ignore_expiration:
            return test and self.expiration == other.expiration
        else:
            return test

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)


_RE_SLAB_STAT = re.compile('^STAT (?P<id>\d+):chunk_size (\d+)$')
_RE_ITEM = re.compile('^ITEM (?P<key>\S+) \[(?P<size>\d+) b; (?P<expiration>\d+) s\]$')

class MemcacheInspector:
    def __init__(self, hosts):
        if isinstance(hosts, (list, tuple)):
            self.clients = self._build_clients(hosts)
        else:
            self.clients = self._build_clients([hosts])

    def _build_clients(self, hosts):
        clients = []
        for host in hosts:
            if isinstance(host, memcache.Client):
                clients.append(host)
            else:
                clients.append(memcache.Client([host]))
        return clients

    def _get_hostname(self, server):
        if server.socket.family == socket.AF_INET:
            return '%s:%s' % (server.ip, server.port)
        else:
            return 'unix:%s' % (server.address,)

    def _get_slabs(self, server):
        server.send_cmd('stats slabs')
        slabs = []
        line = server.readline()
        while line and line != 'END':
            m = _RE_SLAB_STAT.match(line)
            if m:
                slabs.append(m.groupdict()['id'])
            line = server.readline()
        return set(slabs)

    def _get_itemset(self, cache, include_values, max_value_size):
        itemset = {}
        for server in cache.servers:
            if not server.connect():
                continue

            items = {}
            for slab in self._get_slabs(server):
                server.send_cmd('stats cachedump %s 0' % (slab,))
                line = server.readline()
                while line and line != 'END':
                    m = _RE_ITEM.match(line)
                    if m:
                        groups = m.groupdict()
                        if max_value_size <= 0 or int(groups['size']) <= max_value_size:
                            items[groups['key']] = MemcacheItem(groups['key'], int(groups['size']), datetime.datetime.fromtimestamp(int(groups['expiration'])))
                    line = server.readline()

            if include_values and items:
                server.send_cmd('get %s' % ' '.join([i.key for i in items.values()]))
                line = server.readline()
                while line and line != 'END':
                    rkey, flags, rlen = cache._expectvalue(server, line)
                    if rkey is not None:
                        items[rkey].value = cache._recv_value(server, flags, rlen)
                    line = server.readline()

            itemset[self._get_hostname(server)] = filter(lambda v: not include_values or v.value is not None, items.values())

        return itemset

    def get_items(self, include_values=False, max_value_size=0):
        itemsets = {}
        for client in self.clients:
            itemsets.update(self._get_itemset(client, include_values, max_value_size))
        return itemsets


def get_items(hosts, include_values=False, max_value_size=0):
    return MemcacheInspector(hosts).get_items(include_values, max_value_size)

