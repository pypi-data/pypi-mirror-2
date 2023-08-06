import asyncore
import logging

from mopidy.frontends.mpd.server import MpdServer
from mopidy.utils.process import BaseThread

logger = logging.getLogger('mopidy.frontends.mpd.thread')

class MpdThread(BaseThread):
    def __init__(self, core_queue):
        super(MpdThread, self).__init__(core_queue)
        self.name = u'MpdThread'

    def run_inside_try(self):
        logger.debug(u'Starting MPD server thread')
        server = MpdServer(self.core_queue)
        server.start()
        asyncore.loop()
