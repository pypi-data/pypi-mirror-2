import gobject
gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

import logging
import multiprocessing

from mopidy import settings
from mopidy.outputs.base import BaseOutput
from mopidy.utils.process import (BaseThread, pickle_connection,
    unpickle_connection)

logger = logging.getLogger('mopidy.outputs.gstreamer')

class GStreamerOutput(BaseOutput):
    """
    Audio output through GStreamer.

    Starts :class:`GStreamerMessagesThread` and :class:`GStreamerPlayerThread`.

    **Settings:**

    - :attr:`mopidy.settings.GSTREAMER_AUDIO_SINK`
    """

    def __init__(self, *args, **kwargs):
        super(GStreamerOutput, self).__init__(*args, **kwargs)
        # Start a helper thread that can run the gobject.MainLoop
        self.messages_thread = GStreamerMessagesThread(self.core_queue)

        # Start a helper thread that can process the output_queue
        self.output_queue = multiprocessing.Queue()
        self.player_thread = GStreamerPlayerThread(self.core_queue,
            self.output_queue)

    def start(self):
        self.messages_thread.start()
        self.player_thread.start()

    def destroy(self):
        self.messages_thread.destroy()
        self.player_thread.destroy()

    def process_message(self, message):
        assert message['to'] == 'output', \
            u'Message recipient must be "output".'
        self.output_queue.put(message)

    def _send_recv(self, message):
        (my_end, other_end) = multiprocessing.Pipe()
        message['to'] = 'output'
        message['reply_to'] = pickle_connection(other_end)
        self.process_message(message)
        my_end.poll(None)
        return my_end.recv()

    def _send(self, message):
        message['to'] = 'output'
        self.process_message(message)

    def play_uri(self, uri):
        return self._send_recv({'command': 'play_uri', 'uri': uri})

    def deliver_data(self, capabilities, data):
        return self._send({
            'command': 'deliver_data',
            'caps': capabilities,
            'data': data,
        })

    def end_of_data_stream(self):
        return self._send({'command': 'end_of_data_stream'})

    def get_position(self):
        return self._send_recv({'command': 'get_position'})

    def set_position(self, position):
        return self._send_recv({'command': 'set_position', 'position': position})

    def set_state(self, state):
        return self._send_recv({'command': 'set_state', 'state': state})

    def get_volume(self):
        return self._send_recv({'command': 'get_volume'})

    def set_volume(self, volume):
        return self._send_recv({'command': 'set_volume', 'volume': volume})


class GStreamerMessagesThread(BaseThread):
    def __init__(self, core_queue):
        super(GStreamerMessagesThread, self).__init__(core_queue)
        self.name = u'GStreamerMessagesThread'

    def run_inside_try(self):
        gobject.MainLoop().run()


class GStreamerPlayerThread(BaseThread):
    """
    A process for all work related to GStreamer.

    The main loop processes events from both Mopidy and GStreamer.

    Make sure this subprocess is started by the MainThread in the top-most
    parent process, and not some other thread. If not, we can get into the
    problems described at
    http://jameswestby.net/weblog/tech/14-caution-python-multiprocessing-and-glib-dont-mix.html.
    """

    def __init__(self, core_queue, output_queue):
        super(GStreamerPlayerThread, self).__init__(core_queue)
        self.name = u'GStreamerPlayerThread'
        self.output_queue = output_queue
        self.gst_pipeline = None

    def run_inside_try(self):
        self.setup()
        while True:
            message = self.output_queue.get()
            self.process_mopidy_message(message)

    def setup(self):
        logger.debug(u'Setting up GStreamer pipeline')

        self.gst_pipeline = gst.parse_launch(' ! '.join([
            'audioconvert name=convert',
            'volume name=volume',
            settings.GSTREAMER_AUDIO_SINK,
        ]))

        pad = self.gst_pipeline.get_by_name('convert').get_pad('sink')

        if settings.BACKENDS[0] == 'mopidy.backends.local.LocalBackend':
            uri_bin = gst.element_factory_make('uridecodebin', 'uri')
            uri_bin.connect('pad-added', self.process_new_pad, pad)
            self.gst_pipeline.add(uri_bin)
        else:
            app_src = gst.element_factory_make('appsrc', 'appsrc')
            app_src_caps = gst.Caps("""
                audio/x-raw-int,
                endianness=(int)1234,
                channels=(int)2,
                width=(int)16,
                depth=(int)16,
                signed=(boolean)true,
                rate=(int)44100""")
            app_src.set_property('caps', app_src_caps)
            self.gst_pipeline.add(app_src)
            app_src.get_pad('src').link(pad)

        # Setup bus and message processor
        gst_bus = self.gst_pipeline.get_bus()
        gst_bus.add_signal_watch()
        gst_bus.connect('message', self.process_gst_message)

    def process_new_pad(self, source, pad, target_pad):
        pad.link(target_pad)

    def process_mopidy_message(self, message):
        """Process messages from the rest of Mopidy."""
        if message['command'] == 'play_uri':
            response = self.play_uri(message['uri'])
            connection = unpickle_connection(message['reply_to'])
            connection.send(response)
        elif message['command'] == 'deliver_data':
            self.deliver_data(message['caps'], message['data'])
        elif message['command'] == 'end_of_data_stream':
            self.end_of_data_stream()
        elif message['command'] == 'set_state':
            response = self.set_state(message['state'])
            connection = unpickle_connection(message['reply_to'])
            connection.send(response)
        elif message['command'] == 'get_volume':
            volume = self.get_volume()
            connection = unpickle_connection(message['reply_to'])
            connection.send(volume)
        elif message['command'] == 'set_volume':
            response = self.set_volume(message['volume'])
            connection = unpickle_connection(message['reply_to'])
            connection.send(response)
        elif message['command'] == 'set_position':
            response = self.set_position(message['position'])
            connection = unpickle_connection(message['reply_to'])
            connection.send(response)
        elif message['command'] == 'get_position':
            response = self.get_position()
            connection = unpickle_connection(message['reply_to'])
            connection.send(response)
        else:
            logger.warning(u'Cannot handle message: %s', message)

    def process_gst_message(self, bus, message):
        """Process messages from GStreamer."""
        if message.type == gst.MESSAGE_EOS:
            logger.debug(u'GStreamer signalled end-of-stream. '
                'Sending end_of_track to core_queue ...')
            self.core_queue.put({'command': 'end_of_track'})
        elif message.type == gst.MESSAGE_ERROR:
            self.set_state('NULL')
            error, debug = message.parse_error()
            logger.error(u'%s %s', error, debug)
            # FIXME Should we send 'stop_playback' to core here? Can we
            # differentiate on how serious the error is?

    def play_uri(self, uri):
        """Play audio at URI"""
        self.set_state('READY')
        self.gst_pipeline.get_by_name('uri').set_property('uri', uri)
        return self.set_state('PLAYING')

    def deliver_data(self, caps_string, data):
        """Deliver audio data to be played"""
        app_src = self.gst_pipeline.get_by_name('appsrc')
        caps = gst.caps_from_string(caps_string)
        buffer_ = gst.Buffer(buffer(data))
        buffer_.set_caps(caps)
        app_src.set_property('caps', caps)
        app_src.emit('push-buffer', buffer_)

    def end_of_data_stream(self):
        """
        Add end-of-stream token to source.

        We will get a GStreamer message when the stream playback reaches the
        token, and can then do any end-of-stream related tasks.
        """
        self.gst_pipeline.get_by_name('appsrc').emit('end-of-stream')

    def set_state(self, state_name):
        """
        Set the GStreamer state. Returns :class:`True` if successful.

        .. digraph:: gst_state_transitions

            "NULL" -> "READY"
            "PAUSED" -> "PLAYING"
            "PAUSED" -> "READY"
            "PLAYING" -> "PAUSED"
            "READY" -> "NULL"
            "READY" -> "PAUSED"

        :param state_name: NULL, READY, PAUSED, or PLAYING
        :type state_name: string
        :rtype: :class:`True` or :class:`False`
        """
        result = self.gst_pipeline.set_state(
            getattr(gst, 'STATE_' + state_name))
        if result == gst.STATE_CHANGE_FAILURE:
            logger.warning('Setting GStreamer state to %s: failed', state_name)
            return False
        else:
            logger.debug('Setting GStreamer state to %s: OK', state_name)
            return True

    def get_volume(self):
        """Get volume in range [0..100]"""
        gst_volume = self.gst_pipeline.get_by_name('volume')
        return int(gst_volume.get_property('volume') * 100)

    def set_volume(self, volume):
        """Set volume in range [0..100]"""
        gst_volume = self.gst_pipeline.get_by_name('volume')
        gst_volume.set_property('volume', volume / 100.0)
        return True

    def set_position(self, position):
        self.gst_pipeline.get_state() # block until state changes are done
        handeled = self.gst_pipeline.seek_simple(gst.Format(gst.FORMAT_TIME),
            gst.SEEK_FLAG_FLUSH, position * gst.MSECOND)
        self.gst_pipeline.get_state() # block until seek is done
        return handeled

    def get_position(self):
        try:
            position = self.gst_pipeline.query_position(gst.FORMAT_TIME)[0]
            return position // gst.MSECOND
        except gst.QueryError, e:
            logger.error('time_position failed: %s', e)
            return 0
