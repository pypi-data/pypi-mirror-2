
import collections
import time

class ExpiringView(collections.MutableMapping):
    
    def __init__(self, mapping, maxage=None, on_expire=None):
        self.mapping = mapping
        self.maxage = maxage
        if on_expire:
            self.on_expire = on_expire
    
    def __setitem__(self, key, value):
        self.set(key, value)
    
    def _get(self, key):
        pair = self.mapping.get(key)
        if pair and pair[0] is not None and pair[0] < time.time():
            del self.mapping[key]
            self.on_expire(pair[1])
            return None
        return pair
    
    def on_expire(self, value):
        pass
    
    def set(self, key, value, maxage=None):
        if maxage is None:
            maxage = self.maxage
        if maxage is None:
            expiry = None
        else:
            expiry = time.time() + maxage
        self.mapping[key] = (expiry, value)
    
    def setdefault(self, key, value, maxage=None):
        try:
            return self[key]
        except KeyError:
            self.set(key, value, maxage)
            return value
    
    def setdefault_with_call(self, key, callback, maxage=None):
        try:
            return self[key]
        except KeyError:
            value = callback()
            self.set(key, value, maxage)
            return value
        
    def __getitem__(self, key):
        pair = self._get(key)
        if not pair:
            raise KeyError(key)
        return pair[1]
    
    def __delitem__(self, key):
        pair = self._get(key)
        del self.mapping[key]
        if expiry is not None and expiry < time.time():
            raise KeyError(key)
    
    def __iter__(self):
        for key in self.mapping.keys():
            pair = self._get(key)
            if pair:
                yield key
    
    def __len__(self):
        return len(self.mapping)
    
    def collect_garbage(self):
        for x in self:
            pass
    
    def __getattr__(self, name):
        return getattr(self.mapping, name)
    

def on_expire(value):
    print 'expired', repr(value)


if __name__ == '__main__':
    x = ExpiringView({}, maxage=1, on_expire=on_expire)
    x['key'] = 'value'

    print x.items()
    print x['key']
    time.sleep(1)
    print x.items()
    print x['key']