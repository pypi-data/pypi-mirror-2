
import select
import socket
import struct

from erlastic import Atom
from bert.codec import BERTEncoder, BERTDecoder

class Request(object):
    def __init__(self, request_type, module_name, func_name, args, callback=None):
        self.type = request_type
        self.module_name = module_name
        self.func_name = func_name
        self.args = args
        self.callback = callback # (service, mod, fun, args)

    def serialize(self):
        terms = []
        if self.callback:
            terms.append((Atom('info'), Atom('callback'),
                [(Atom('service'), self.callback[0]),
                 (Atom('mfs', self.callback[1], self.callback[2], self.callback[3]))]))
        terms.append((Atom(self.type), Atom(self.module_name), Atom(self.func_name), list(self.args)))
        return terms

class Response(object):
    def __init__(self, connection, response_type, result, cache_access=None, cache_expiration=None):
        self.connection = connection
        self.type = response_type
        self.result = result

class BERTRPCConnection(object):
    def __init__(self, addr):
        if isinstance(addr, tuple):
            self.host, self.port = addr
        else:
            self.host, self.port = addr.split(':')
            self.port = int(self.port)
        self._sock = None
        self._decoder = BERTDecoder()
        self._encoder = BERTEncoder()

    def connect(self):
        if self._sock:
            # Make sure the connection is alive. Assume there shouldn't be any data to read.
            rd, wr, ex = select.select([self._sock], [], [self._sock], 0)
            if rd or ex:
                self._sock.close()
                self._sock = None
        if not self._sock:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self.host, self.port))
        return self._sock

    def send_terms(self, terms):
        binary = []
        for term in terms:
            encoded = self._encoder.encode(term)
            binary.append(struct.pack(">L", len(encoded)))
            binary.append(encoded)
        bytes = "".join(binary)
        self._sock.send(bytes)

    def receive_term(self):
        ln = struct.unpack(">L", self._sock.recv(4))[0]
        encoded = self._sock.recv(ln)
        return self._decoder.decode(encoded)

    def transaction(self, request_terms):
        self.connect()
        self.send_terms(request_terms)
        res = []
        while True:
            response = self.receive_term()
            res.append(response)
            if response[0] != "info":
                break
        return res

    def execute(self, request):
        request_terms = request.serialize()
        response_terms = self.transaction(request_terms)
        options = response_terms[:-1]
        response_type = response_terms[-1][0]
        result = response_terms[-1][1] if len(response_terms[-1]) > 1 else None
        return Response(self, response_type, result, options)
