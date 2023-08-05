


import collections
import logging
from eventlet.green import httplib
import os
import sys
import urllib
import eventlet
from paste import urlmap
import static

import eventlet.wsgi

from csp.eventlet import Listener
import rtjp.eventlet

from errors import ExpectedException
import channel
import rest
import protocol
from user import User

try:
    import json
except:
    import simplejson as json

from config import config
class EmptyLogShim(object):
    def write(self, *args, **kwargs):
        return


class HookboxServer(object):

    def __init__(self, interface, port):
        self.interface = interface
        self.port = port
        self._rtjp_server = rtjp.eventlet.RTJPServer()
#        self.identifer_key = 'abc';
        self.base_host = config['cbhost']
        self.base_port = config['cbport']
        self.base_path = config['cbpath']
        self.app = urlmap.URLMap()
        self.csp = Listener()
        self.app['/csp'] = self.csp
        static_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'static')
        self.app['/static'] = static.Cling(static_path)
        self.app['/rest'] = rest.HookboxRest(self)

        self.channels = {}
        self.conns_by_cookie = {}
        self.conns = {}


    def run(self):
        print "Listening to hookbox on http://%s:%s" % (self.interface or "0.0.0.0", self.port)
        eventlet.spawn(eventlet.wsgi.server, eventlet.listen((self.interface, self.port)), self.app, log=EmptyLogShim())
        ev = eventlet.event.Event()
        self._rtjp_server.listen(sock=self.csp)
        eventlet.spawn(self._run, ev)
        return ev

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

    def _run(self, ev):
        # NOTE: You probably want to call this method directly if you're trying
        #       To use some other wsgi server than eventlet.wsgi
        while True:
            try:
                rtjp_conn = self._rtjp_server.accept().wait()
                conn = protocol.HookboxConn(self, rtjp_conn)
            except:
                ev.send_exception(*sys.exc_info())
                break
        print "HookboxServer Stopped"


    def http_request(self, path_name, cookie_string=None, form={}):
        path = self.base_path + '/' + config.get('cb_' + path_name)
        if config['secret']:
            form['secret'] = config['secret']
        body = urllib.urlencode(form)
        http = httplib.HTTPConnection(self.base_host, self.base_port)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        if cookie_string:
            headers['Cookie'] = cookie_string
        http.request('POST', path, body=body, headers=headers)
        response = http.getresponse()
        if response.status != 200:
            raise ExpectedException("Invalid callback response, status=%s (%s)" % (response.status, path))
        body = response.read()
        try:
           output = json.loads(body)
        except:
            raise ExpectedException("Invalid json: " + body)
        if not isinstance(output, list) or len(output) != 2:
            raise ExpectedException("Invalid response (expected json list of length 2)")
        if not isinstance(output[1], dict):
            raise ExpectedException("Invalid response (expected json object in response index 1)")
        output[1] = dict([(str(k), v) for (k,v) in output[1].items()])
        return output

    def connect(self, conn):
        form = { 'conn_id': conn.id }
        success, options = self.http_request('connect', conn.get_cookie(), form)
        if not success:
            raise ExpectedException(options.get('error', 'Unauthorized'))
        if 'name' not in options:
            raise ExpectedException('Unauthorized (missing name parameter in server response)')
        user = User(self, options['name'])
        user.add_connection(conn)
        self.maybe_auto_subscribe(user, options)

    def create_channel(self, conn, channel_name, **options):
        if channel_name in self.channels:
            raise ExpectedException("Channel already exists")
        cookie_string = conn and conn.get_cookie() or None
        form = {
            'channel_name': channel_name,
        }
        success, options = self.http_request('create_channel', cookie_string, form)
        if not success:
            raise ExpectedException(options.get('error', 'Unauthorized'))

        self.channels[channel_name] = channel.Channel(self, channel_name, **options)



    def destroy_channel(self, channel_name, **options):
        if channel_name not in channels:
            return None
        channel = self.channels[channel_name]
        del self.channels[channel_name]
        channel.destroy()

    def get_channel(self, conn, channel_name):
        if channel_name not in self.channels:
            self.create_channel(conn, channel_name)
        return self.channels[channel_name]

    def maybe_auto_subscribe(self, user, options):
        for destination in options.get('auto_subscribe', ()):
            channel = self.get_channel(channel_name)
            channel.subscribe(user, needs_auth=False)
        for destination in options.get('auto_unsubscribe', ()):
            channel = self.get_channel(channel_name)
            channel.unsubscribe(user, needs_auth=False)
