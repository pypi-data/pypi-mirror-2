import logging
import multiprocessing
import optparse

from mopidy import get_version, settings
from mopidy.utils import get_class
from mopidy.utils.log import setup_logging
from mopidy.utils.path import get_or_create_folder, get_or_create_file
from mopidy.utils.process import BaseProcess, unpickle_connection
from mopidy.utils.settings import list_settings_optparse_callback

logger = logging.getLogger('mopidy.core')

class CoreProcess(BaseProcess):
    def __init__(self):
        super(CoreProcess, self).__init__(name='CoreProcess')
        self.core_queue = multiprocessing.Queue()
        self.options = self.parse_options()
        self.output_queue = None
        self.backend = None
        self.frontend = None

    def parse_options(self):
        parser = optparse.OptionParser(version='Mopidy %s' % get_version())
        parser.add_option('-q', '--quiet',
            action='store_const', const=0, dest='verbosity_level',
            help='less output (warning level)')
        parser.add_option('-v', '--verbose',
            action='store_const', const=2, dest='verbosity_level',
            help='more output (debug level)')
        parser.add_option('--dump',
            action='store_true', dest='dump',
            help='dump debug log to file')
        parser.add_option('--list-settings',
            action='callback', callback=list_settings_optparse_callback,
            help='list current settings')
        return parser.parse_args()[0]

    def run_inside_try(self):
        logger.info(u'-- Starting Mopidy --')
        self.setup()
        while True:
            message = self.core_queue.get()
            self.process_message(message)

    def setup(self):
        self.setup_logging()
        self.setup_settings()
        self.output_queue = self.setup_output(self.core_queue)
        self.backend = self.setup_backend(self.core_queue, self.output_queue)
        self.frontend = self.setup_frontend(self.core_queue, self.backend)

    def setup_logging(self):
        setup_logging(self.options.verbosity_level, self.options.dump)

    def setup_settings(self):
        get_or_create_folder('~/.mopidy/')
        get_or_create_file('~/.mopidy/settings.py')
        settings.validate()

    def setup_output(self, core_queue):
        output_queue = multiprocessing.Queue()
        get_class(settings.OUTPUT)(core_queue, output_queue)
        return output_queue

    def setup_backend(self, core_queue, output_queue):
        return get_class(settings.BACKENDS[0])(core_queue, output_queue)

    def setup_frontend(self, core_queue, backend):
        frontend = get_class(settings.FRONTENDS[0])()
        frontend.start_server(core_queue)
        frontend.create_dispatcher(backend)
        return frontend

    def process_message(self, message):
        if message.get('to') == 'output':
            self.output_queue.put(message)
        elif message['command'] == 'mpd_request':
            response = self.frontend.dispatcher.handle_request(
                message['request'])
            connection = unpickle_connection(message['reply_to'])
            connection.send(response)
        elif message['command'] == 'end_of_track':
            self.backend.playback.on_end_of_track()
        elif message['command'] == 'stop_playback':
            self.backend.playback.stop()
        elif message['command'] == 'set_stored_playlists':
            self.backend.stored_playlists.playlists = message['playlists']
        else:
            logger.warning(u'Cannot handle message: %s', message)
