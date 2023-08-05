from copy import copy
import logging
import random
import time

from mopidy import settings
from mopidy.backends.base.current_playlist import BaseCurrentPlaylistController
from mopidy.backends.base.library import BaseLibraryController
from mopidy.backends.base.playback import BasePlaybackController
from mopidy.backends.base.stored_playlists import BaseStoredPlaylistsController
from mopidy.frontends.mpd import translator
from mopidy.models import Playlist
from mopidy.utils import get_class

logger = logging.getLogger('mopidy.backends.base')

__all__ = ['BaseBackend', 'BasePlaybackController',
    'BaseCurrentPlaylistController', 'BaseStoredPlaylistsController',
    'BaseLibraryController']

class BaseBackend(object):
    """
    :param core_queue: a queue for sending messages to
        :class:`mopidy.process.CoreProcess`
    :type core_queue: :class:`multiprocessing.Queue`
    :param output_queue: a queue for sending messages to the output process
    :type output_queue: :class:`multiprocessing.Queue`
    :param mixer_class: either a mixer class, or :class:`None` to use the mixer
        defined in settings
    :type mixer_class: a subclass of :class:`mopidy.mixers.BaseMixer` or
        :class:`None`
    """

    def __init__(self, core_queue=None, output_queue=None, mixer_class=None):
        self.core_queue = core_queue
        self.output_queue = output_queue
        if mixer_class is None:
            mixer_class = get_class(settings.MIXER)
        self.mixer = mixer_class(self)

    #: A :class:`multiprocessing.Queue` which can be used by e.g. library
    #: callbacks executing in other threads to send messages to the core
    #: thread, so that action may be taken in the correct thread.
    core_queue = None

    #: The current playlist controller. An instance of
    #: :class:`mopidy.backends.base.BaseCurrentPlaylistController`.
    current_playlist = None

    #: The library controller. An instance of
    # :class:`mopidy.backends.base.BaseLibraryController`.
    library = None

    #: The sound mixer. An instance of :class:`mopidy.mixers.BaseMixer`.
    mixer = None

    #: The playback controller. An instance of
    #: :class:`mopidy.backends.base.BasePlaybackController`.
    playback = None

    #: The stored playlists controller. An instance of
    #: :class:`mopidy.backends.base.BaseStoredPlaylistsController`.
    stored_playlists = None

    #: List of URI prefixes this backend can handle.
    uri_handlers = []

    def destroy(self):
        """
        Call destroy on all sub-components in backend so that they can cleanup
        after themselves.
        """

        if self.current_playlist:
            self.current_playlist.destroy()

        if self.library:
            self.library.destroy()

        if self.mixer:
            self.mixer.destroy()

        if self.playback:
            self.playback.destroy()

        if self.stored_playlists:
            self.stored_playlists.destroy()
