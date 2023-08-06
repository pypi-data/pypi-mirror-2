"""
    bjson/handlers.py
    
    Asynchronous Bidirectional JSON-RPC protocol implementation over TCP/IP
    
    Copyright (c) 2010 David Martinez Marti
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    1. Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of copyright holders nor the names of its
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
    PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL COPYRIGHT HOLDERS OR CONTRIBUTORS
    BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

"""
import re
from types import MethodType
from bjsonrpc.exceptions import  ServerError

class BaseHandler(object):
    """
        Base Class to publish remote methods. It is instantiated by *Connection*.
        
        Example::
        
            class MyHandler(bjson.handlers.BaseHandler):
                def _setup(self):
                    # Initailize here.
                    self.c = 0
                    
                def echo(self,text): 
                    print text
                    self.c += 1
                    
                def getcount(self): return c
    """
    
    public_methods_pattern = r'^[a-z]\w+$'
    # Pattern to know which methods should be automatically published
    
    nonpublic_methods = [
        "close",
        "add_method",
        "get_method",
        ] 
    # List of method names that never should be published    
        
    def __init__(self, connection):
        if hasattr(connection,"connection"): 
            self._conn = connection.connection
        else:
            self._conn = connection
            
        self._methods = {}
        for mname in dir(self):
            if re.match(self.public_methods_pattern, mname):
                function = getattr(self, mname)
                if isinstance(function, MethodType):
                    self.add_method(function)
            
        self._setup()
        
    def _setup(self):
        """
            Empty method to ease inheritance. Overload it with your needs, it
            will be called after __init__.
        """
        pass 
        
    def close(self):
        """
            Cleans some variables before the object is freed. _close is called
            manually from connection whenever a handler is going to be deleted.
        """
        self._methods = {}

    def add_method(self, *args, **kwargs):
        """
            Porcelain for publishing methods into the handler. Is used by the
            constructor itself to publish all non-private functions.
        """
        for method in args:
            if method.__name__ in self.nonpublic_methods: 
                continue
            assert(method.__name__ not in self._methods)
            self._methods[method.__name__] = method
            
        for name, method in kwargs.iteritems():
            if method.__name__ in self.nonpublic_methods: 
                continue
            assert(name not in self._methods)
            self._methods[name] = method

    def get_method(self, name):
        """
            Porcelain for resolving method objects from their names. Used by
            connections to get the apropiate method object.
        """
        if name not in self._methods:
            raise ServerError("Unknown method %s" % repr(name))
            
        return self._methods[name]
        

class NullHandler(BaseHandler):
    """
        Null version of BaseHandler which has nothing in it. Use this when you
        don't want to publish any function.
    """
    pass

