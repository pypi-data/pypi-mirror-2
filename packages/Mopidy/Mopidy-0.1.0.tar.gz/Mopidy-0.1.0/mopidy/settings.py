"""
Available settings and their default values.

.. warning::

    Do *not* change settings directly in :mod:`mopidy.settings`. Instead, add a
    file called ``~/.mopidy/settings.py`` and redefine settings there.
"""

#: List of playback backends to use. See :mod:`mopidy.backends` for all
#: available backends.
#:
#: Default::
#:
#:     BACKENDS = (u'mopidy.backends.libspotify.LibspotifyBackend',)
#:
#: .. note::
#:     Currently only the first backend in the list is used.
BACKENDS = (
    u'mopidy.backends.libspotify.LibspotifyBackend',
)

#: The log format used on the console. See
#: http://docs.python.org/library/logging.html#formatter-objects for details on
#: the format.
CONSOLE_LOG_FORMAT = u'%(levelname)-8s %(asctime)s' + \
    ' [%(process)d:%(threadName)s] %(name)s\n  %(message)s'

#: The log format used for dump logs.
#:
#: Default::
#:
#:     DUMP_LOG_FILENAME = CONSOLE_LOG_FORMAT
DUMP_LOG_FORMAT = CONSOLE_LOG_FORMAT

#: The file to dump debug log data to when Mopidy is run with the
#: :option:`--dump` option.
#:
#: Default::
#:
#:     DUMP_LOG_FILENAME = u'dump.log'
DUMP_LOG_FILENAME = u'dump.log'

#: List of server frontends to use.
#:
#: Default::
#:
#:     FRONTENDS = (u'mopidy.frontends.mpd.MpdFrontend',)
#:
#: .. note::
#:     Currently only the first frontend in the list is used.
FRONTENDS = (u'mopidy.frontends.mpd.MpdFrontend',)

#: Which GStreamer audio sink to use in :mod:`mopidy.outputs.gstreamer`.
#:
#: Default::
#:
#:     GSTREAMER_AUDIO_SINK = u'autoaudiosink'
GSTREAMER_AUDIO_SINK = u'autoaudiosink'

#: Path to folder with local music.
#:
#: Used by :mod:`mopidy.backends.local`.
#:
#: Default::
#:
#:    LOCAL_MUSIC_FOLDER = u'~/music'
LOCAL_MUSIC_FOLDER = u'~/music'

#: Path to playlist folder with m3u files for local music.
#:
#: Used by :mod:`mopidy.backends.local`.
#:
#: Default::
#:
#:    LOCAL_PLAYLIST_FOLDER = u'~/.mopidy/playlists'
LOCAL_PLAYLIST_FOLDER = u'~/.mopidy/playlists'

#: Path to tag cache for local music.
#:
#: Used by :mod:`mopidy.backends.local`.
#:
#: Default::
#:
#:    LOCAL_TAG_CACHE = u'~/.mopidy/tag_cache'
LOCAL_TAG_CACHE = u'~/.mopidy/tag_cache'

#: Sound mixer to use. See :mod:`mopidy.mixers` for all available mixers.
#:
#: Default::
#:
#:     MIXER = u'mopidy.mixers.gstreamer_software.GStreamerSoftwareMixer'
MIXER = u'mopidy.mixers.gstreamer_software.GStreamerSoftwareMixer'

#: ALSA mixer only. What mixer control to use. If set to :class:`False`, first
#: ``Master`` and then ``PCM`` will be tried.
#:
#: Example: ``Master Front``. Default: :class:`False`
MIXER_ALSA_CONTROL = False

#: External mixers only. Which port the mixer is connected to.
#:
#: This must point to the device port like ``/dev/ttyUSB0``.
#:
#: Default: :class:`None`
MIXER_EXT_PORT = None

#: External mixers only. What input source the external mixer should use.
#:
#: Example: ``Aux``. Default: :class:`None`
MIXER_EXT_SOURCE = None

#: External mixers only. What state Speakers A should be in.
#:
#: Default: :class:`None`.
MIXER_EXT_SPEAKERS_A = None

#: External mixers only. What state Speakers B should be in.
#:
#: Default: :class:`None`.
MIXER_EXT_SPEAKERS_B = None

#: The maximum volume. Integer in the range 0 to 100.
#:
#: If this settings is set to 80, the mixer will set the actual volume to 80
#: when asked to set it to 100.
#:
#: Default::
#:
#:     MIXER_MAX_VOLUME = 100
MIXER_MAX_VOLUME = 100

#: Audio output handler to use.
#:
#: Default::
#:
#:     OUTPUT = u'mopidy.outputs.gstreamer.GStreamerOutput'
OUTPUT = u'mopidy.outputs.gstreamer.GStreamerOutput'

#: Which address Mopidy's MPD server should bind to.
#:
#:Examples:
#:
#: ``127.0.0.1``
#:     Listens only on the IPv4 loopback interface. Default.
#: ``::1``
#:     Listens only on the IPv6 loopback interface.
#: ``0.0.0.0``
#:     Listens on all IPv4 interfaces.
#: ``::``
#:     Listens on all interfaces, both IPv4 and IPv6.
MPD_SERVER_HOSTNAME = u'127.0.0.1'

#: Which TCP port Mopidy's MPD server should listen to.
#:
#: Default: 6600
MPD_SERVER_PORT = 6600

#: Path to the libspotify cache.
#:
#: Used by :mod:`mopidy.backends.libspotify`.
SPOTIFY_LIB_CACHE = u'~/.mopidy/libspotify_cache'

#: Your Spotify Premium username.
#:
#: Used by :mod:`mopidy.backends.libspotify`.
SPOTIFY_USERNAME = u''

#: Your Spotify Premium password.
#:
#: Used by :mod:`mopidy.backends.libspotify`.
SPOTIFY_PASSWORD = u''
