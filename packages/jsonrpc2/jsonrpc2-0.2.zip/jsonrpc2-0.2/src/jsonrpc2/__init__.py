# -*- coding:utf-8 -*-

"""
http://groups.google.com/group/json-rpc/web/json-rpc-2-0

errors:

code 	message 	meaning
-32700 	Parse error 	Invalid JSON was received by the server.
An error occurred on the server while parsing the JSON text.
-32600 	Invalid Request 	The JSON sent is not a valid Request object.
-32601 	Method not found 	The method does not exist / is not available.
-32602 	Invalid params 	Invalid method parameter(s).
-32603 	Internal error 	Internal JSON-RPC error.
-32099 to -32000 	Server error 	Reserved for implementation-defined server-errors.

"""
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
errors = {}
errors[PARSE_ERROR] = "Parse Error"
errors[INVALID_REQUEST] = "Invalid Request"
errors[METHOD_NOT_FOUND] = "Method Not Found"
errors[INVALID_PARAMS] = "Invalid Params"
errors[INTERNAL_ERROR] = "Internal Error"
import sys
try:
    import json
except ImportError:
    try:
        import django.utils.simplejson as json
        sys.modules['json'] = json
    except ImportError:
        import simplejson as json
        sys.modules['json'] = json

import itertools

class JsonRpcException(Exception):
    """
    >>> exc = JsonRpcException(1, INVALID_REQUEST)
    >>> str(exc)
    '{"jsonrpc": "2.0", "id": 1, "error": {"message": "Invalid Request", "code": -32600}}'

    """

    def __init__(self, rpc_id, code, data=None):
        self.rpc_id = rpc_id
        self.code = code
        self.data = data
    
    @property
    def message(self):
        return errors[self.code]

    def as_dict(self):
        if self.data:
            return {'jsonrpc':'2.0',
                'id': self.rpc_id,
                'error':{'code': self.code,
                        'message':self.message,
                        'data':self.data}}
        else:
            return {'jsonrpc':'2.0',
                'id': self.rpc_id,
                'error':{'code': self.code,
                        'message':self.message}}

    def __str__(self):
        return json.dumps(self.as_dict())

class JsonRpcBase(object):
    def __init__(self, methods=None):
        if methods is not None:
            self.methods = methods
        else:
            self.methods = {}

    def process(self, data):

        if data.get('jsonrpc') != "2.0":
            raise JsonRpcException(data.get('id'), INVALID_REQUEST)

        if 'method' not in data:
            raise JsonRpcException(data.get('id'), INVALID_REQUEST)
        
        methodname = data['method']
        if not isinstance(methodname, basestring):
            raise JsonRpcException(data.get('id'), INVALID_REQUEST)
            
        if methodname.startswith('_'):
            raise JsonRpcException(data.get('id'), METHOD_NOT_FOUND)


        if methodname not in self.methods:
            raise JsonRpcException(data.get('id'), METHOD_NOT_FOUND)


        method = self.methods[methodname]
        try:
            params = data.get('params', [])
            if isinstance(params, list):
                result = method(*params)
            elif isinstance(params, dict):
                result = method(**dict([(str(k), v) for k, v in params.iteritems()]))
            else:
                raise JsonRpcException(data.get('id'), METHOD_NOT_FOUND)
            resdata = None
            if data.get('id'):

                resdata = {
                    'jsonrpc':'2.0',
                    'id':data.get('id'),
                    'result':result,
                    }
            return resdata
        except Exception, e:
            raise JsonRpcException(data.get('id'), INTERNAL_ERROR, data=str(e))

    def _call(self, data):
        try:
            return self.process(data)
        except JsonRpcException, e:
            return e.as_dict()

    def __call__(self, data):
        if isinstance(data, dict):
            resdata = self._call(data)
        elif isinstance(data, list):
            if len([x for x in data if not isinstance(x, dict)]):
                resdata = {'jsonrpc':'2.0',
                            'id':None,
                            'error':{'code':INVALID_REQUEST,
                                    'message':errors[INVALID_REQUEST]}}
            else:
                resdata = [d for d in (self._call(d) for d in data) if d is not None]
            
        return resdata


class JsonRpc(JsonRpcBase):
    def __init__(self, methods=None):
        super(JsonRpc, self).__init__(methods)

    def addModule(self, mod):
        name = mod.__name__
        for k, v in ((k, v) for k, v in mod.__dict__.iteritems() if not k.startswith('_') and callable(v)):
            self.methods[name + '.' + k] = v



class JsonRpcApplication(object):
    def __init__(self, rpcs=None):
        self.rpc = JsonRpc(rpcs)


    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] != "POST":
            start_response('405 Method Not Allowed',
                    [('Content-type', 'text/plain')])
            return ["405 Method Not Allowed"]

        if environ['CONTENT_TYPE'] != 'application/json':
            start_response('400 Bad Request',
                    [('Content-type', 'text/plain')])
            return ["Content-type must by application/json"]

        try:
            body = environ['wsgi.input'].read(-1)
            data = json.loads(body)
            resdata = self.rpc(data) 
        except ValueError, e:
            resdata = {'jsonrpc':'2.0',
                       'id':None,
                       'error':{'code':PARSE_ERROR,
                                'message':errors[PARSE_ERROR]}}

        start_response('200 OK',
                [('Content-type', 'application/json')])


        if resdata:
            return [json.dumps(resdata)]
        return []


def make_app(global_conf, **app_conf):
    conf = global_conf.copy()
    conf.update(app_conf)

    modname = conf["module"]
    __import__(modname)
    mod = sys.modules[modname]
    obj = eval(conf["expression"], mod.__dict__)
    return JsonRpcApplication(obj)

