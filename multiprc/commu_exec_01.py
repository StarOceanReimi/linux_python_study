import multiprocessing
import urllib2
import urllib
def cookiedict_tostr(cookiedict):
    assert cookiedict is not None, 'cookiedict cant be None'
    return ';'.join(["%s=%s" % (k, urllib.urlencode(v, True)) for k, v in cookiedict])

class HttpResourceGetterTask(object):
    
    def __init__(self, url=None, headers=None, cookies=None, **params):
        assert url is not None, 'url cant be None'
        self.url = url
        if headers is None:
            headers = {}
        if cookies is not None:
            headers.setdefault('Cookie', cookiedict_tostr(cookies))
        self.headers = headers
        self.params = params

    def to_urlrequest(self):
        if self.params is None:
            req = urllib2.Request(self.url, headers=self.headers)
        else:
            req = urllib2.Request(self.url, headers=self.headers, data=urllib.urlencode(self.params, True))
        return req

def worker(q):
    while True:
        obj = q.get()
        if obj is None:
            break
        req = obj.to_urlrequest()
        print req

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()
    queue.put(HttpResourceGetterTask(url='http://example.com'))
    queue.put(HttpResourceGetterTask(url='http://www.google.com'))
    queue.put(None)
    queue.close()
    queue.join_thread()
    p.join()
