import urllib
import httplib
import json
import socket
import stopam

USER_AGENT = 'Stopam Python Client {0}'.format(stopam.VERSION)

DEFAULTS = {
    'host': 'stopam.com',
    'port': 80,
    'timeout': 1
}

__all__ = ['Error', 'TimeoutError', 'InvalidApiKeyError', 
    'ServiceUnreachableError', 'Question', 'Service']


class Error(Exception): 
    message = 'Service error'
    
    def __init__(self, value=None):
        super(Error, self).__init__(value or self.message)

class TimeoutError(Error): 
    message = 'Timeout'

class InvalidApiKeyError(Error): 
    message = 'Invalid api key'

class ServiceUnreachableError(Error): 
    message = 'Service is unreachable'


class Question(object):
    def __init__(self, question, token):
        self.question = question
        self.token = token
    
    def __str__(self):
        return "{0} (token: {1})".format(self.question, self.token)


class _RealService(object):
    
    def __init__(self, key, timeout, host, port):
        self.key = key
        self.timeout = timeout
        self.host = host
        self.port = port

        self._need_reconnect = True
        self._c = None
        
    def _connect(self):
        self._c = httplib.HTTPConnection(self.host, 
                                         self.port, 
                                         timeout=self.timeout)
        
    def _reconnect(self):
        self.close()
        self._connect()
        
    def _reconnect_if_necessary(self):
        if self._need_reconnect:
            self._reconnect()
            
    def _request(self, path, body):
        body = urllib.urlencode(body)
        
        response, status, data = None, None, None
        tried_reconnect = False
        
        try:
            while not tried_reconnect:
                self._reconnect_if_necessary()
                # Sometimes the connection has been closed so we
                # use a loop to retry up to 3 times.
                try:
                    self._c.request('POST', path, body, 
                                    {'User-Agent': USER_AGENT})
                    response = self._c.getresponse()
                    status = response.status
                    data = response.read()
                    break
                except httplib.BadStatusLine:
                    # The connection has been closed - retry
                    tried_reconnect = True
                    self._need_reconnect = True
            
            if status in [200, 400]:
                return (status, data)
            elif status == 403:
                raise InvalidApiKeyError("Invalid API key: '{0}'".format(self.key))
            else:
                raise Error('Unknown error. Response code: {0}, Data: {1}'.format(status, data))
            
        except socket.timeout:
            raise TimeoutError('Timed out after {0} seconds.'.format(self.timeout))
        except socket.error as e:
            raise ServiceUnreachableError(str(e))
        finally:
            if response:
                response.close()
        
    def ask(self):
        (_status, data) = self._request('/api/ask/', {'key': self.key})
        
        js = json.loads(data)
        return Question(token=js['token'], question=js['question'])
        
        
    def verify(self, token, answer):
        (status, _data) = self._request('/api/verify/', {'key': self.key,
                                                         'answer': answer,
                                                         'token': token})
        return status == 200
        
    def close(self):
        if self._c:
            self._c.close()
        
        
class _DummyService(object):
    TOKEN = '00000000000000'
    
    def ask(self):
        return Question('How much is 2+2?', self.TOKEN)
    
    def verify(self, _token, answer):
        return str(answer) == '4'
    
    def close(self):
        pass
        

class Service(object):
    """
    This is the main class that you need to access the Stopam service.
    Usage is simple::
    
        >>> with Service('05631bb4e55a434c9ef71c6daf9e2cdd') as c:
        ...     q = c.ask()
        ...     answer = raw_input(q.question) # How much is 3+3? (for example) 
        ...     if c.verify(q.token, answer):
        ...         print('valid') # if the user entered 6
        ...     else:
        ...         print('failed') # otherwise
        'valid'
    
    `Service` accepts a few arguments:
        
        :param key: This is the key that you obtain
            from the stopam site.
            
        :param fallback: If this parameter is set to `True` the service will
            use a dummy provider for the questions. This is to guarantee that 
            in the event of network (or other) failure your application will
            continue to work. 
            
            Default is `True`, but for development - set it to `False` - it 
            will help you see the error (if any).
            
        :param timeout: (optional) This is the timeout for the request, 
            in seconds.
        
            If it expires when a question is being asked with `fallback=True` it
            will fallback to the internal question provider. If it expires while
            answering `verify()` will return `False`. The fallback provider has
            no way of knowing the answer.
            
            If `fallback=False` an `TimeoutError` will be raised in both cases.
            
            Default: 30
    
        If you don't use the `with` statement make sure you call `close()` on
        the end to close the connection.
        
        The service may raise a few exceptions:
        
            `TimeoutError`: when a request (either ask or verify) times out.

            `InvalidApiKeyError`: when the API key is not correct.

            `ServiceUnreachableError`: when the service is unreachable

    """
    def __init__(self, key, timeout=None, fallback=True, host=None, port=None):
        self.key = key
        
        self._real = _RealService(key, 
                                  timeout or DEFAULTS['timeout'], 
                                  host or DEFAULTS['host'],
                                  port or DEFAULTS['port'])
        self._dummy = _DummyService()
        self.fallback = fallback
            
    def ask(self):
        try:
            return self._real.ask()
        except:
            if not self.fallback: raise
            
            return self._dummy.ask()
    
    def verify(self, token, answer):
        if token == _DummyService.TOKEN:
            return self._dummy.verify(token, answer)
        else:
            try:
                return self._real.verify(token, answer)
            except:
                if not self.fallback: raise
                # The question is from the service - dummy will always
                # return False, as it doesn't know the answer - so no
                # need to ask it.
                return False
    
    def __enter__(self):
        return self
        
    def close(self):
        try:
            self._real.close()
        except:
            if not self.fallback: raise
            # else swallow it 
        
    def __exit__(self, _type, _value, _traceback):
        self.close()