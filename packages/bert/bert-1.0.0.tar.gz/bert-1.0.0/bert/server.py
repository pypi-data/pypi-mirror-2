
import logging
import random
import time
import asyncore
import socket
import struct
from multiprocessing import Pool

from erlastic import Atom
from bert import decode, encode

DEFAULT_PORT = 9000

class Client(asyncore.dispatcher):
    def __init__(self, sock, addr, server, manager):
        asyncore.dispatcher.__init__(self, sock)
        self.addr = addr
        self.server = server
        self.manager = manager
        self.in_buffer = ""
        self.out_buffer = ""
        self.in_terms = []

    def writable(self):
        return len(self.out_buffer) != 0

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(8192)
        if not data:
            self.close()
            return

        self.in_buffer += data

        bytes_left = len(self.in_buffer)

        while bytes_left > 4:
            berp_len = struct.unpack(">L", self.in_buffer[:4])[0]
            if bytes_left < 4 + berp_len:
                break

            berp = self.in_buffer[4:4+berp_len]
            self.in_buffer = buffer(self.in_buffer, 4+berp_len)
            bytes_left -= 4+berp_len

            term = decode(berp)
            self.in_terms.append(term)
            if term[0] != "info":
                self.handle_request(self.in_terms)
                self.in_terms = []

    def handle_write(self):
        if len(self.out_buffer) == 0:
            return 0

        try:
            nsent = self.send(self.out_buffer)
        except socket.error, e:
            self.close()
            return

        self.out_buffer = buffer(self.out_buffer, nsent)

    def send_buffered(self, data):
        self.out_buffer += data
        self.handle_write()

    def send_terms(self, terms):
        binary = []
        for term in terms:
            encoded = encode(term)
            binary.append(struct.pack(">L", len(encoded)))
            binary.append(encoded)
        bytes = "".join(binary)
        self.send_buffered(bytes)

    # def receive_term(self):
    #     ln = struct.unpack(">L", self._sock.recv(4))[0]
    #     encoded = self._sock.recv(ln)
    #     return self._decoder.decode(encoded)

    def handle_request(self, terms):
        request_type = terms[-1][0]
        if request_type not in ("call", "cast"):
            logging.error("Received unknown request type %s" % request_type)
            return

        module_name = terms[-1][1]
        func_name = terms[-1][2]
        args = terms[-1][3]

        if request_type == "call":
            res = self.server.call(module_name, func_name, args, callback=self.call_callback)
        elif request_type == "cast":
            self.server.call(module_name, func_name, args)
            self.send_terms([(Atom("noreply"),)])

    def call_callback(self, result):
        print "<<", result
        self.send_terms([(Atom("reply"), result)])

class Manager(object):
    pass

def dispatch(modules, module_name, func_name, args):
    print ">>>", module_name, func_name, args
    func = getattr(modules[module_name], func_name)
    try:
        return func(*args)
    except:
        return "ERROR"

class BERTRPCServer(asyncore.dispatcher):
    def __init__(self, modules, host="127.0.0.1", port=DEFAULT_PORT):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.modules = modules
        self.manager = Manager()
        self.worker_pool = Pool(1)

    def handle_accept(self):
        sock, addr = self.accept()
        Client(sock, addr, self, self.manager)

    def start(self):
        self.running = True
        while self.running:
            asyncore.loop(timeout=1, use_poll=False, count=1)

    def stop(self):
        self.running = False

    def call(self, module_name, func_name, args, callback=None):
        self.worker_pool.apply_async(dispatch, (self.modules, module_name, func_name, args), callback=callback)
