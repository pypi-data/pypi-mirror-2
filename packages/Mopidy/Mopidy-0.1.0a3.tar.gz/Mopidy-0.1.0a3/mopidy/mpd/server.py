"""
This is our MPD server implementation.
"""

import asynchat
import asyncore
import logging
import multiprocessing
import re
import socket
import sys

from mopidy import get_mpd_protocol_version, settings
from mopidy.utils import indent, pickle_connection

logger = logging.getLogger('mopidy.mpd.server')

#: The MPD protocol uses UTF-8 for encoding all data.
ENCODING = u'utf-8'

#: The MPD protocol uses ``\n`` as line terminator.
LINE_TERMINATOR = u'\n'

class MpdServer(asyncore.dispatcher):
    """
    The MPD server. Creates a :class:`MpdSession` for each client connection.
    """

    def __init__(self, core_queue):
        asyncore.dispatcher.__init__(self)
        self.core_queue = core_queue

    def start(self):
        try:
            if socket.has_ipv6:
                self.create_socket(socket.AF_INET6, socket.SOCK_STREAM)
            else:
                self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            hostname = self._format_hostname(settings.SERVER_HOSTNAME)
            port = settings.SERVER_PORT
            logger.debug(u'Binding to [%s]:%s', hostname, port)
            self.bind((hostname, port))
            self.listen(1)
            logger.info(u'MPD server running at [%s]:%s',
                self._format_hostname(settings.SERVER_HOSTNAME),
                settings.SERVER_PORT)
        except IOError, e:
            sys.exit('MPD server startup failed: %s' % e)

    def handle_accept(self):
        (client_socket, client_socket_address) = self.accept()
        logger.info(u'MPD client connection from [%s]:%s',
            client_socket_address[0], client_socket_address[1])
        MpdSession(self, client_socket, client_socket_address,
            self.core_queue).start()

    def handle_close(self):
        self.close()

    def _format_hostname(self, hostname):
        if (socket.has_ipv6
            and re.match('\d+.\d+.\d+.\d+', hostname) is not None):
            hostname = '::ffff:%s' % hostname
        return hostname


class MpdSession(asynchat.async_chat):
    """
    The MPD client session. Dispatches MPD requests to the frontend.
    """

    def __init__(self, server, client_socket, client_socket_address,
            core_queue):
        asynchat.async_chat.__init__(self, sock=client_socket)
        self.server = server
        self.client_address = client_socket_address[0]
        self.client_port = client_socket_address[1]
        self.core_queue = core_queue
        self.input_buffer = []
        self.set_terminator(LINE_TERMINATOR.encode(ENCODING))

    def start(self):
        self.send_response(u'OK MPD %s' % get_mpd_protocol_version())

    def collect_incoming_data(self, data):
        self.input_buffer.append(data)

    def found_terminator(self):
        data = ''.join(self.input_buffer).strip()
        self.input_buffer = []
        try:
            request = data.decode(ENCODING)
            logger.debug(u'Input from [%s]:%s: %s', self.client_address,
                self.client_port, indent(request))
            self.handle_request(request)
        except UnicodeDecodeError as e:
            logger.warning(u'Received invalid data: %s', e)

    def handle_request(self, request):
        my_end, other_end = multiprocessing.Pipe()
        self.core_queue.put({
            'command': 'mpd_request',
            'request': request,
            'reply_to': pickle_connection(other_end),
        })
        my_end.poll(None)
        response = my_end.recv()
        if response is not None:
            self.handle_response(response)

    def handle_response(self, response):
        self.send_response(LINE_TERMINATOR.join(response))

    def send_response(self, output):
        logger.debug(u'Output to [%s]:%s: %s', self.client_address,
            self.client_port, indent(output))
        output = u'%s%s' % (output, LINE_TERMINATOR)
        data = output.encode(ENCODING)
        self.push(data)
