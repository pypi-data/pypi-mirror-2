from __future__ import absolute_import
from concurrence import dispatch, Tasklet, Message
from concurrence.io import BufferedStream, Socket, Server
from concurrence.core import Channel

from . import core

import logging
try:
    import json
except ImportError:
    import simplejson as json


class Event(object):
    def __init__(self):
        self._channel = Channel()
    
    def send(self, arg, block=False):
        if not block and not self._channel.has_receiver():
            print 'need a Tasklet'
            Tasklet.new(self._send)(arg)
            print 'blah'
            return None
        return self._channel.send(arg)
    
    def _send(self, arg):
        print 'in _send'
        self._channel.send(arg)
    
    def send_exception(self, e):
        return self._channel.send_exception(e.__class__, e.args)
        
    def wait(self):
        print 'waiting on', self._channel, self._channel.has_sender(), self._channel.has_receiver()
        return self._channel.receive()
        


class RTJPServer(object):
    
    def __init__(self):
        self._sock = None
        self._accept_channel = Channel()
        
    def listen(self, port, interface=""):
        e = Event()
        e.send(None)
        Server.serve((interface, port), self._accept_incoming)
#        Tasklet.new(self._listen)(port, interface)
        return e
        
#    def _listen(self, port, interface):
#        print 'call Server.serve'
#    def __listen(self)
#        dispatch(Server.serve, (interface, port), self._accept_incoming)
#        print 'done calling Server.serve'
        
    def _accept_incoming(self, sock):
        print 'rtjp.concurrence.RTJPServer._accept'
        c = RTJPConnection(sock)
        self._accept_channel.send(c)
        return True
        
    def accept(self):
        ev = Event()
        if self._accept_channel.has_sender():
            ev.send(self._accept_channel.receive())
        else:
            Tasklet.new(self._accept)(ev)
        return ev

    def _accept(self, ev):
        ev.send(self._accept_channel.receive())


class RTJPConnection(object):
    logger = logging.getLogger('RTJPConnection')
    
    def __init__(self, sock, delimiter='\r\n'):
        self._sock = sock
        self.frame_id = 0
        self.stream = BufferedStream(sock)
        self._frame_channel = Channel()
        self.delimiter = delimiter
        t = Tasklet.new(self._read_forever)()
        
        
    def close(self):
        self._sock.close()
        
    def _read_forever(self):
        lines = self.stream.reader.read_lines()
        while True:
            print 'read a line...'
            try:
                raw_frame = lines.next()
            except Exception, e:
                print 'a problem:', repr(e)
                self._frame_channel.send_exception(Exception, "Connection Lost")
                return
            print 'READ', raw_frame
            try:
                frame = core.deserialize_frame(raw_frame)
            except core.RTJPParseException, e:
                self.send_error(e.id, e.args[0])
                # error?
                continue
            print 'frame is', frame
            self._frame_channel.send(frame)
        print 'done..'
        
    def recv_frame(self):
        print 'recv_frame'
        ev = Event()
        if self._frame_channel.has_sender():
            ev.send(self._frame_channel.receive())
        else:
            Tasklet.new(self._recv_frame)(ev)
        return ev
        
    def _recv_frame(self, ev):
        print '_recv_frame'
        try:
            ev.send(self._frame_channel.receive())
        except Exception, e:
            ev.send_exception(e)


    def send_frame(self, name, args={}):
        self.logger.debug('send_frame', name, args)
        self.frame_id += 1
        raw_frame = json.dumps([self.frame_id, name, args]) + self.delimiter
        ev = Event()
        Tasklet.new(self._send_frame)(raw_frame, ev)
        return ev
    
    def _send_frame(self, raw_frame, ev):
        print "SEND", raw_frame
        try:
            self.stream.writer.write_bytes(raw_frame)
            self.stream.writer.flush()
        except Exception, e:
            ev.send_exception(e)
        else:
            ev.send(None)
    
    def send_error(self, reference_id, msg):
        return self.send_frame('ERROR', { 'reference_id': reference_id, 'msg': str(msg) })
        
      