import collections
import logging
from eventlet.green import httplib
import os
import sys
import urllib
import urlparse
import eventlet
from paste import urlmap
import static

import eventlet.wsgi
import eventlet.websocket

from csp_eventlet import Listener
import rtjp_eventlet

from errors import ExpectedException
import channel
import rest
import protocol
from user import User
from admin.admin import HookboxAdminApp


try:
    import json
except:
    import simplejson as json

class EmptyLogShim(object):
    def write(self, *args, **kwargs):
        return

logger = logging.getLogger('hookbox')

class HookboxServer(object):

    def __init__(self, bound_socket, config, outputter):
        self.config = config
        self.interface = config['interface']
        self.port = config['port']
        self._bound_socket = bound_socket
        self._rtjp_server = rtjp_eventlet.RTJPServer()
#        self.identifer_key = 'abc';
        self.base_host = config['cbhost']
        self.base_port = config['cbport']
        self.base_path = config['cbpath']
            
        self.app = urlmap.URLMap()
        self.csp = Listener()
        self.app['/csp'] = self.csp
        self.app['/ws'] = self._ws_wrapper
        self._ws_wsgi_app = eventlet.websocket.WebSocketWSGI(self._ws_wsgi_app)
        
        static_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'static')
        self.app['/static'] = static.Cling(static_path)
        self.app['/rest'] = rest.HookboxRest(self, config)
        self.admin = HookboxAdminApp(self, config, outputter)
        self.app['/admin'] = self.admin
        self.channels = {}
        self.conns_by_cookie = {}
        self.conns = {}
        self.users = {}

    def _ws_wrapper(self, environ, start_response):
        environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
        environ['SCRIPT_NAME'] = ''
        return self._ws_wsgi_app(environ, start_response)

    def _ws_wsgi_app(self, ws):
        sock = SockWebSocketWrapper(ws)
        rtjp_conn = rtjp_eventlet.RTJPConnection(sock=sock)
        self._accept(rtjp_conn)
        
    def run(self):
        print "Listening to hookbox on http://%s:%s" % (self.interface or "0.0.0.0", self.port)
        if not self._bound_socket:
            self._bound_socket = eventlet.listen((self.interface, self.port))
#        el
        eventlet.spawn(eventlet.wsgi.server, self._bound_socket, self.app, log=EmptyLogShim())
        ev = eventlet.event.Event()
        self._rtjp_server.listen(sock=self.csp)
        eventlet.spawn(self._run, ev)
        return ev

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

    def _accept(self, rtjp_conn):
        conn = protocol.HookboxConn(self, rtjp_conn, self.config)
        conn.run()

    def _run(self, ev):
        # NOTE: You probably want to call this method directly if you're trying
        #       To use some other wsgi server than eventlet.wsgi
        while True:
            try:
                rtjp_conn = self._rtjp_server.accept().wait()
                eventlet.spawn(self._accept, rtjp_conn)
#                conn = protocol.HookboxConn(self, rtjp_conn, self.config)
            except:
                ev.send_exception(*sys.exc_info())
                break
        print "HookboxServer Stopped"

    def http_request(self, path_name=None, cookie_string=None, form={}, full_path=None):
        if not full_path and self.config['cb_single_url']:
            full_path = self.config['cb_single_url']
        if full_path:
            u = urlparse.urlparse(full_path)
            host = u.hostname
            port = u.port or 80
            path = u.path
            if u.query:
                path += '?' + u.query
        else:
#            if self.config.get('cb_single_url'):
#                path = self.config["cbpath"]
#                host = self.base_host
#            else:
            path = self.base_path + '/' + self.config.get('cb_' + path_name)
            host = self.config["cbhost"]
            port = self.config["cbport"]
        
        if path_name:
            form['action'] = path_name
        if self.config['webhook_secret']:
            form['secret'] = self.config['webhook_secret']
        # TODO: The following code creates a hideously bloated form_body. I'm
        #       sure we actually have to use urlencode for this.
        # TODO: I rolled back the unicode fix, because its broken...
        #       -mcarter 6/27/10
        for key, val in form.items():
            new_key = key
            if isinstance(key, unicode):
                del form[key]
                new_key = key.encode('utf-8')
            new_val = val
            if isinstance(val, unicode):
                new_val = val.encode('utf-8')
            form[new_key] = new_val

        form_body = urllib.urlencode(form)
        # TODO: stash this, and re-use it; maybe it will do keep alive too!
        #       -mcarter 5/28/10
        http = httplib.HTTPConnection(host, port)
        
        # for logging
        url = "http://" + host
        if port != 80:
            url += ":" + str(self.base_port)
        url += path
        
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        if cookie_string:
            headers['Cookie'] = cookie_string
        body = None
        try:
            http.request('POST', path, body=form_body, headers=headers)
            response = http.getresponse()
            body = response.read()
        except Exception, e:
            import traceback
            self.admin.webhook_event(path_name, url, 0, False, body, form_body, cookie_string, e)
            traceback.print_exc()
            return False, {}
        if response.status != 200:
            self.admin.webhook_event(path_name, url, response.status, False, body, form_body, cookie_string, "Invalid status")
            raise ExpectedException("Invalid callback response, status=%s (%s), body: %s" % (response.status, path, body))
        try:
           output = json.loads(body)
        except:
            self.admin.webhook_event(path_name, url, response.status, False, body, form_body, cookie_string, "Invalid json response")
            raise ExpectedException("Invalid json: " + body)
        #print 'response to', path, 'is:', output
        if not isinstance(output, list) or len(output) != 2:
            self.admin.webhook_event(path_name, url, response.status, False, body, form_body, cookie_string, "len(response) != 2 (list)")
            raise ExpectedException("Invalid response (expected json list of length 2)")
        if not isinstance(output[1], dict):
            self.admin.webhook_event(path_name, url, response.status, False, body, form_body, cookie_string, "response[1] != json object")
            raise ExpectedException("Invalid response (expected json object in response index 1)")
        output[1] = dict([(str(k), v) for (k,v) in output[1].items()])
        err = ""
        if not output[0]:
            err = output[1].get('msg', "(No reason given)")
        self.admin.webhook_event(path_name, url, response.status, output[0], body, form_body, cookie_string, err)
        return output

        # type, url, response status, success/failture, raw_output

#    def _webhook_error

    def connect(self, conn):
        form = { 'conn_id': conn.id }
        success, options = self.http_request('connect', conn.get_cookie(), form)
        if not success:
            raise ExpectedException(options.get('error', 'Unauthorized'))
        if 'name' not in options:
            raise ExpectedException('Unauthorized (missing name parameter in server response)')
        self.conns[conn.id] = conn
        user = self.get_user(options['name'])
        user.add_connection(conn)
        self.admin.user_event('connect', user.get_name(), conn.serialize())
        self.admin.connection_event('connect', conn.id, conn.serialize())
        #print 'successfully connected', user.name
        eventlet.spawn(self.maybe_auto_subscribe, user, options, conn=conn)

    def disconnect(self, conn):
        self.admin.user_event('disconnect', conn.user.get_name(), { "id": conn.id})
        self.admin.connection_event('disconnect', conn.id, conn.serialize())
        del self.conns[conn.id]

    def get_connection(self, id):
        return self.conns.get(id, None)
        
    def exists_user(self, name):
        return name in self.users
    def get_user(self, name):
        if name not in self.users:
            self.users[name] = User(self, name)
            self.admin.user_event('create', name, self.users[name].serialize())
        return self.users[name]

    def remove_user(self, name):
        if name in self.users:
            self.admin.user_event('destroy', name, {})
            user = self.users[name]
            del self.users[name]
            form = { 'name': name }
            try:
                self.http_request('disconnect', user.get_cookie(), form)
            except ExpectedException, e:
                pass
            except Exception, e:
                self.logger.warn("Unexpected error when removing user: %s", e, exc_info=True)
        
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
        chan = self.channels[channel_name]
        self.admin.channel_event('create_channel', channel_name, chan.serialize())
        


    def destroy_channel(self, channel_name, needs_auth=True):
        if channel_name not in self.channels:
            return None
        channel = self.channels[channel_name]
        if channel.destroy(needs_auth):
            del self.channels[channel_name]
            self.admin.channel_event('destroy_channel', channel_name, None)

    def exists_channel(self, channel_name):
        return channel_name in self.channels

    def get_channel(self, conn, channel_name):
        if channel_name not in self.channels:
            self.create_channel(conn, channel_name)
        return self.channels[channel_name]

    def maybe_auto_subscribe(self, user, options, conn=None):
        #print 'maybe autosubscribe....'
        for destination in options.get('auto_subscribe', ()):
            #print 'subscribing to', destination
            channel = self.get_channel(user, destination)
            channel.subscribe(user, conn=conn, needs_auth=False)
        for destination in options.get('auto_unsubscribe', ()):
            channel = self.get_channel(user, destination)
            channel.unsubscribe(user, conn=conn, needs_auth=False)



class SockWebSocketWrapper(object):
    def __init__(self, ws):
        self._ws = ws
        
    def recv(self, num):
        # not quite right (ignore num)... but close enough for our use.
        data = self._ws.wait()
        if data:
            data = data.encode('utf-8')
        return data

    def send(self, data):
        self._ws.send(data)
        return len(data)
        
    def sendall(self, data):
        self.send(data)
        
    def __getattr__(self, key):
        return getattr(self._ws, key)