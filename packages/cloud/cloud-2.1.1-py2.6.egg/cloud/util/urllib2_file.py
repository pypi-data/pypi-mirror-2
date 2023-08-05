#!/usr/bin/env python
####
# Heavily modified version of urllib2_file. Original docs follow:
# Version 1.0 (PiCloud):
#  - Support gzip compression each way, use python2.5 http interface, etc.
#  - Add support for persistent HTTP Connections
# Version: 0.2.0
#  - UTF-8 filenames are now allowed (Eli Golovinsky)<br/>
#  - File object is no more mandatory, Object only needs to have seek() read() attributes (Eli Golovinsky)<br/>
#
# Version: 0.1.0
#  - upload is now done with chunks (Adam Ambrose)
#
# Version: older
# THANKS TO:
# bug fix: kosh @T aesaeion.com
# HTTPS support : Ryan Grow <ryangrow @T yahoo.com>
# Copyright (C) 2004,2005,2006 Fabien SEISEN
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
# you can contact me at: <fabien@seisen.org>
# http://fabien.seisen.org/python/
#
# Also modified by Adam Ambrose (aambrose @T pacbell.net) to write data in
# chunks (hardcoded to CHUNK_SIZE for now), so the entire contents of the file
# don't need to be kept in memory.
#

"""
enable to upload files using multipart/form-data

idea from:
upload files in python:
 http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306

timeoutsocket.py: overriding Python socket API:
 http://www.timo-tasi.org/python/timeoutsocket.py
 http://mail.python.org/pipermail/python-announce-list/2001-December/001095.html

import urllib2_files
import urllib2
u = urllib2.urlopen('http://site.com/path' [, data])

data can be a mapping object or a sequence of two-elements tuples
(like in original urllib2.urlopen())
varname still need to be a string and
value can be string of a file object
eg:
  ((varname, value),
   (varname2, value),
  )
  or
  { name:  value,
    name2: value2
  }

"""

import os
import socket
import sys
import stat
import thread
import mimetypes
#BUG in python 2.6 mimetypes: We must call init() here to ensure thread safety
if not mimetypes.inited:
    mimetypes.init()

import email.generator as generator
import random
import httplib
import urllib
import urllib2
from cStringIO import StringIO

import logging
cloudLog = logging.getLogger('Cloud.HTTPConnection')


CHUNK_SIZE = 65536


#PiCloud injection for gzip control
from .. import cloudconfig as cc

use_gzip = cc.transportConfigurable('use_gzip',
                                     default=True,hidden=False,
                                     comment='Request gziped HTTP responses')
client_gzip = False #gzip http requests? (genreally don't use this)

http_close_connection = cc.transportConfigurable('http_close',
                                     default=False,hidden=False,
                                     comment='Should every HTTP connection be closed after receiving a response?')

#new:
from .gzip_stream import GzipFile
#from gzip import GzipFile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def choose_boundary():
    """Choose boundary with more randomness
    Pray that it doesn't conflict :)"""
    _fmt = generator._fmt
    boundary = ('=' * 8)
    for i in range(8):          
        token = random.randrange(sys.maxint)
        boundary += _fmt % token
    boundary += '=='
    return boundary

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def send_data(v_vars, v_files, boundary, gzip = True, sock = None):
    """Either returns data or sends in depending on arguments.
    
    Return value is a tuple of string data, content-length
    
    Content-length always returns; it represents the content-length of the http request
    
    If sock is None:
        Typically string data is returned; this can be written straight to the socket
        
        However, as an optimization, if any v_files correspond to a file on disk and gzip is false,
            The data returned will be none. This must then call send_data again with sock nonnull
    
    If sock is a connection, content-length will be returned AND data will be streamed over socket (but not returned) 
        direct socket writing will not work if gzip is True as content-length of http request will be wrong
    """
    
    all_in_memory = True  #if we can return this
    cl = 0 #holds content_length
    
    if gzip: 
        if sock:
            raise TypeError('gzip and sock cannot both be true')  
        gzip_file = StringIO()
        buffer = GzipFile(filename=None,fileobj=gzip_file,mode='w')
    else:
        buffer = StringIO()

    
    for (k, v) in v_vars:
        #buffer=''
        buffer.write('--%s\r\n' % boundary)
        buffer.write('Content-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (k,v))
    
    for (k, v) in v_files:
        fd = v
        contents = None
        try:  #check if String IO
            contents = fd.getvalue()
            file_size = len(contents)
            name = k
        except AttributeError, e:
            #This might be a file on disk
            try:
                assert not gzip #if gzipping is true, we must fall back to reading in file
                file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
                
            except (AssertionError, AttributeError, OSError), e: #not a physical file -- must read in
                fd.seek(0)
                contents = fd.read() 
                file_size = len(contents)
            
            try:
                name = fd.name.split('/')[-1]
                if isinstance(name, unicode):
                    name = name.encode('UTF-8')
            except AttributeError: #no name? revert to k 
                name = k

        buffer.write('--%s\r\n' % boundary)
        buffer.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' \
                  % (k, name))
        buffer.write('Content-Type: %s\r\n' % get_content_type(name))
        buffer.write('Content-Length: %s\r\n' % file_size)        
        
        buffer.write('\r\n')

        if not contents:
            all_in_memory = False
        
        if sock or not all_in_memory:
            assert not gzip #sanity check
            
            #reset buffer and update content-length if not returning result                
            buf_str = buffer.getvalue()            
            buffer.close()   
            cl += len(buf_str)
            buffer = StringIO() #regen buffer
            cl += file_size  
            
            if sock:                
                sock.sendall(buf_str)
                
                if contents:
                    sock.sendall(contents)
                else:
                    if hasattr(fd, 'seek'):
                        fd.seek(0)
    
                    data=fd.read(CHUNK_SIZE)
                    while data:
                            sock.sendall(data)
                            data=fd.read(CHUNK_SIZE)
            
        
        elif all_in_memory: #keep writing into RAM
            buffer.write(contents)

            

    buffer.write('\r\n--%s--\r\n\r\n' % boundary)   
    
    if sock or not all_in_memory:
        buf_str = buffer.getvalue()
        if sock:
            sock.sendall(buf_str)        
        cl += len(buf_str)
        return None, cl        
    
    #in memory
    #When Using compressed content_len = compressed length (gzip
    # we need mod_wsgi middleware on the django server
    if gzip:
        buffer.close()
        buf_str = gzip_file.getvalue()
    else:        
        buf_str = buffer.getvalue()        
    return buf_str, len(buf_str)

def makeBodyFunction(v_vars, v_files, boundary):
    def theBody(httpcon):
        try:
            send_data(v_vars, v_files, boundary, gzip = False, sock = httpcon.sock)
        except socket.error, v:
            if v[0] == 32:      # Broken pipe
                httpcon.close()
            raise
    return theBody


class funcBodyHTTPConnection(httplib.HTTPConnection):
    """
    httplib connection that supports calling a function to handle body sending
    body takes a single argument -- this connection. 
    Note that automatic content-length calculation is not done if body is a function
    
    Also supports persistant
    """
    
    def _send_request(self, method, url, body, headers):
    
        if callable(body):
            httplib.HTTPConnection._send_request(self, method, url, None, headers)
            body(self)
        else:
            httplib.HTTPConnection._send_request(self, method, url, body, headers)
        


# modified version from urllib2
class newHTTPAbstractHandler(urllib2.AbstractHTTPHandler):

    def __init__(self, debuglevel=0):
        urllib2.AbstractHTTPHandler.__init__(self, debuglevel)
        self.connections = {}
    
    def do_open(self, http_class, req):
        """Adds ability to reuse connections
        """
        host = req.get_host()
        if not host:
            raise urllib2.URLError('no host given')

        conn_key = host, http_class, thread.get_ident()  #good enough for picloud
        #print 'conn_key is ', conn_key
        h = self.connections.get(conn_key)
        if h:
            #print 'found!', h.sock
            reuse = True
        if not h:  #no cached conn - reconnect
            if hasattr(req,'timeout'):
                h = http_class(host, timeout=req.timeout) # will parse host:port
            else:
                h = http_class(host)  #py2.5
            h.set_debuglevel(self._debuglevel)
            self.connections[conn_key] = h
            reuse = False

        headers = dict(req.headers)
        headers.update(req.unredirected_hdrs)
        # We want to make an HTTP/1.1 request, but the addinfourl
        # class isn't prepared to deal with a persistent connection.
        # It will try to read all remaining data from the socket,
        # which will block while the server waits for the next request.
        # So make sure the connection gets closed after the (only)
        # request.
        
        if http_close_connection:
            headers["Connection"] = "close"
        headers = dict(
            (name.title(), val) for name, val in headers.items())

        if hasattr(req, 'tunnel_host') and req._tunnel_host: #py2.5 lacks this
            tunnel_headers = {}
            proxy_auth_hdr = "Proxy-Authorization"
            if proxy_auth_hdr in headers:
                tunnel_headers[proxy_auth_hdr] = headers[proxy_auth_hdr]
                # Proxy-Authorization should not be sent to origin
                # server.
                del headers[proxy_auth_hdr]
            h._set_tunnel(req._tunnel_host, headers=tunnel_headers)

        for i in range(2): 
            #persistent connection handling via httplib2 
            try:
                h.request(req.get_method(), req.get_selector(), req.data, headers)
            except socket.gaierror, err:
                h.close()
                raise urllib2.URLError(err)
            except (socket.error, httplib.HTTPException):
                #may still have response
                pass
            try:
                #print 'sock is', h.sock
                r = h.getresponse()
                #print 'post-end is', h.sock, r.will_close
            except Exception, err:  #known exceptions are (socket.error, httplib.HTTPException, AttributeError)
                #print 'socket closed!!', str(err)
                #socket closed -- retry?
                
                if i == 0 and reuse:
                    cloudLog.debug('Reconnecting socket due to error %s',  str(err))
                    h.close()
                    h.connect()
                    continue
                    #raise  urllib2.URLError(err)
                else:
                    raise  urllib2.URLError(err)
            break


        # Pick apart the HTTPResponse object to get the addinfourl
        # object initialized properly.

        # Wrap the HTTPResponse object in socket's file object adapter
        # for Windows.  That adapter calls recv(), so delegate recv()
        # to read().  This weird wrapping allows the returned object to
        # have readline() and readlines() methods.

        # XXX It might be better to extract the read buffering code
        # out of socket._fileobject() and into a base class.

        r.recv = r.read
        fp = socket._fileobject(r, close=False)  #set close to false to leave conn open

        resp = urllib2.addinfourl(fp, r.msg, req.get_full_url())
        resp.code = r.status
        resp.msg = r.reason
        
        return resp


    def do_request_(self, request):
        """Modified to support multipart data"""
        
        host = request.get_host()
        if not host:
            raise urllib2.URLError('no host given')

        if not request.has_data():
            request = urllib2.AbstractHTTPHandler.do_request_(self, request)
        else:
            data = request.get_data()
            
            v_files=[]
            v_vars=[]
            # mapping object (dict)
            if type(data) == str:
                request = urllib2.AbstractHTTPHandler.do_request_(self, request)
            else:                         
                if hasattr(data, 'items'):
                    data = list(data.items())
                else:
                    try:
                        if len(data) and not isinstance(data[0], tuple):
                            raise TypeError
                    except TypeError:
                        ty, va, tb = sys.exc_info()
                        raise TypeError("not a valid non-string sequence or mapping object").with_traceback(tb)
                    
                for (k, v) in data:
                    if hasattr(v, 'read'):
                        v_files.append((k, v))
                    else:
                        v_vars.append( (k, v) )
                        
                if len(v_files) == 0:
                    if v_vars:
                        data = urllib.urlencode(v_vars)
                    else:
                        data = ""                      
                    if not request.has_header('Content-type'):
                        request.add_unredirected_header('Content-Type',
                                    'application/x-www-form-urlencoded')
                        request.add_unredirected_header('Content-length', '%d' % len(data))
                
                elif not request.has_header('Content-type') and len(v_files) > 0:
                        boundary = choose_boundary()
                        gzip_request = client_gzip and getattr(request,'use_gzip',False)
                        
                        data, content_len = send_data(v_vars, v_files, boundary, gzip_request)
                        request.add_unredirected_header('Content-Type',
                                    'multipart/form-data; boundary=%s' % boundary)
                        request.add_unredirected_header('Content-length', str(content_len))
                        
                        #gzip outbound requests:
                        if (gzip_request):
                            request.add_unredirected_header('Content-Encoding', 'gzip')
                
                #request's data is none if we need to do further evaluation
                if data is not None:
                    request.data = data
                else: #use callback
                    request.data = makeBodyFunction(v_vars, v_files, boundary)
                            
                #final steps (from urllib2.AbstractHTTPHandler)
                sel_host = host
                if hasattr(request,'has_proxy') and request.has_proxy():
                    scheme, sel = urllib.splittype(request.get_selector())
                    sel_host, sel_path = urllib.splithost(sel)
        
                if not request.has_header('Host'):
                    request.add_unredirected_header('Host', sel_host)
                for name, value in self.parent.addheaders:
                    name = name.capitalize()
                    if not request.has_header(name):
                        request.add_unredirected_header(name, value)              

        if (use_gzip):
            request.add_unredirected_header('Accept-Encoding', 'gzip')
            #pass

        return request
        
    def do_response_(self, request, response):         
        #print 'type', fp.__class__
        if response.headers and response.headers.getheader('Content-Encoding','') == 'gzip':
                                        
            fp = GzipFile(filename=None,fileobj=StringIO(response.read()),mode='r')
            #fp = GzipFile(filename=None,fileobj=response,mode='r')
            #response needs to be StringIO(response.read()) without gzip streaming

            old_response = response
            response = urllib.addinfourl(fp, old_response.headers, old_response.url)
            if hasattr(old_response,'code'):
                response.code = old_response.code
            response.msg = old_response.msg
        return response

class newHTTPHandler(newHTTPAbstractHandler):
    http_request = newHTTPAbstractHandler.do_request_
    http_response = newHTTPAbstractHandler.do_response_
    
    def http_open(self, req):
        return self.do_open(funcBodyHTTPConnection, req)    

if hasattr(httplib, 'HTTPS'):
    class funcBodyHTTPSConnection(httplib.HTTPSConnection):
        """
        See docs for funcBodyHTTPConnection
        """
        
        def _send_request(self, method, url, body, headers):
            if callable(body):
                httplib.HTTPSConnection._send_request(self, method, url, None, headers)
                body(self)
            else:
                httplib.HTTPSConnection._send_request(self, method, url, body, headers)    
    
    class newHTTPSHandler(newHTTPAbstractHandler):
        https_request = newHTTPAbstractHandler.do_request_
        https_response = newHTTPAbstractHandler.do_response_
        
        def https_open(self, req):
            return self.do_open(funcBodyHTTPSConnection, req)    

#Input handling
_opener = None

#modified urlopen - supports python 2.5 and 2.6
def urlopen(url, data=None, timeout = None):
    global _opener
    if _opener is None:
        _opener = build_opener()
    if not timeout:
        if not hasattr(socket,'_GLOBAL_DEFAULT_TIMEOUT'):
            #python 2.5
            return _opener.open(url, data)
        else:
            timeout=socket._GLOBAL_DEFAULT_TIMEOUT
    return _opener.open(url, data, timeout)

#modified build_opener:
def build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP and FTP.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    import types
    def isclass(obj):
        return isinstance(obj, types.ClassType) or hasattr(obj, "__bases__")

    opener = urllib2.OpenerDirector()
    default_classes = [urllib2.ProxyHandler, urllib2.UnknownHandler, newHTTPHandler,
                       urllib2.HTTPDefaultErrorHandler, urllib2.HTTPRedirectHandler,
                       urllib2.FTPHandler, urllib2.FileHandler, urllib2.HTTPErrorProcessor]
    if hasattr(httplib, 'HTTPS'):
        default_classes.append(newHTTPSHandler)
    skip = set()
    for klass in default_classes:
        for check in handlers:
            if isclass(check):
                if issubclass(check, klass):
                    skip.add(klass)
            elif isinstance(check, klass):
                skip.add(klass)
    for klass in skip:
        default_classes.remove(klass)

    for klass in default_classes:
        opener.add_handler(klass())

    for h in handlers:
        if isclass(h):
            h = h()
        opener.add_handler(h)
    return opener
