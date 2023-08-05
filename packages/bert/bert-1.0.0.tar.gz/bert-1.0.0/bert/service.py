
from bert.connection import BERTRPCConnection, Request

class Dispatcher(object):
    def __init__(self, parent, name):
        self._parent = parent
        self._cache = {}
        self._name = name

    def __getattr__(self, name):
        if name not in self._cache:
            self._cache[name] = Dispatcher(self, name)
        return self._cache[name]

    def __call__(self, *args, **kwargs):
        return self._parent(self._name, *args, **kwargs)

class BERTPCException(Exception):
    def __init__(self, error_type, code, detail, backtrace):
        self.error_type = error_type
        self.code = code
        self.detail = detail
        self.backtrace = backtrace

    def __str__(self):
        return "BERT-RPC Error (%s:%d): %s\n%s" % (self.error_type, self.code, self.detail, "\n".join(self.backtrace))

class ExceptionCreator(object):
    def __getattr__(self, name):
        clas = type(name, (BERTPCException,), {})
        setattr(self, name, clas)
        return clas

class BERTRPCService(object):
    def __init__(self, addr):
        self._connection = BERTRPCConnection(addr)
        self.call = Dispatcher(self, "call")
        self.cast = Dispatcher(self, "cast")
        self.exception = ExceptionCreator()

    def __call__(self, request_type, module_name, func_name, *args, **kwargs):
        if request_type not in ('call', 'cast'):
            raise TypeError("Only requests of type 'call' and 'cast' are supported")
        request = Request(request_type, module_name, func_name, args, **kwargs)
        response = self._connection.execute(request)
        if response.type == "reply":
            return response.result
        elif response.type == "error":
            # {error, {Type, Code, Class, Detail, Backtrace}}
            error_type, code, error_class, detail, backtrace = response.result
            raise getattr(self.exception, error_class.replace(':', '_'))(error_type, code, detail, backtrace)
