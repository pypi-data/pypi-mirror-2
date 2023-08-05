from copy import copy
import logging
import random
import time

from mopidy import settings
from mopidy.models import Playlist
from mopidy.mpd import serializer
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
    :param mixer: either a mixer instance, or :class:`None` to use the mixer
        defined in settings
    :type mixer: :class:`mopidy.mixers.BaseMixer` or :class:`None`
    """

    def __init__(self, core_queue=None, mixer=None):
        self.core_queue = core_queue
        if mixer is not None:
            self.mixer = mixer
        else:
            self.mixer = get_class(settings.MIXER)()

    #: A :class:`multiprocessing.Queue` which can be used by e.g. library
    #: callbacks executing in other threads to send messages to the core
    #: thread, so that action may be taken in the correct thread.
    core_queue = None

    #: The current playlist controller. An instance of
    #: :class:`BaseCurrentPlaylistController`.
    current_playlist = None

    #: The library controller. An instance of :class:`BaseLibraryController`.
    library = None

    #: The sound mixer. An instance of :class:`mopidy.mixers.BaseMixer`.
    mixer = None

    #: The playback controller. An instance of :class:`BasePlaybackController`.
    playback = None

    #: The stored playlists controller. An instance of
    #: :class:`BaseStoredPlaylistsController`.
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

class BaseCurrentPlaylistController(object):
    """
    :param backend: backend the controller is a part of
    :type backend: :class:`BaseBackend`
    """

    #: The current playlist version. Integer which is increased every time the
    #: current playlist is changed. Is not reset before Mopidy is restarted.
    version = 0

    def __init__(self, backend):
        self.backend = backend
        self._cp_tracks = []

    def destroy(self):
        """Cleanup after component."""
        pass

    @property
    def cp_tracks(self):
        """
        List of two-tuples of (CPID integer, :class:`mopidy.models.Track`).

        Read-only.
        """
        return [copy(ct) for ct in self._cp_tracks]

    @property
    def tracks(self):
        """
        List of :class:`mopidy.models.Track` in the current playlist.

        Read-only.
        """
        return [ct[1] for ct in self._cp_tracks]

    def add(self, track, at_position=None):
        """
        Add the track to the end of, or at the given position in the current
        playlist.

        :param track: track to add
        :type track: :class:`mopidy.models.Track`
        :param at_position: position in current playlist to add track
        :type at_position: int or :class:`None`
        :rtype: two-tuple of (CPID integer, :class:`mopidy.models.Track`) that
            was added to the current playlist playlist
        """
        assert at_position <= len(self._cp_tracks), \
            u'at_position can not be greater than playlist length'
        cp_track = (self.version, track)
        if at_position is not None:
            self._cp_tracks.insert(at_position, cp_track)
        else:
            self._cp_tracks.append(cp_track)
        self.version += 1
        return cp_track

    def clear(self):
        """Clear the current playlist."""
        self.backend.playback.stop()
        self.backend.playback.current_cp_track = None
        self._cp_tracks = []
        self.version += 1

    def get(self, **criteria):
        """
        Get track by given criterias from current playlist.

        Raises :exc:`LookupError` if a unique match is not found.

        Examples::

            get(cpid=7)             # Returns track with CPID 7
                                    # (current playlist ID)
            get(id=1)               # Returns track with ID 1
            get(uri='xyz')          # Returns track with URI 'xyz'
            get(id=1, uri='xyz')    # Returns track with ID 1 and URI 'xyz'

        :param criteria: on or more criteria to match by
        :type criteria: dict
        :rtype: two-tuple (CPID integer, :class:`mopidy.models.Track`)
        """
        matches = self._cp_tracks
        for (key, value) in criteria.iteritems():
            if key == 'cpid':
                matches = filter(lambda ct: ct[0] == value, matches)
            else:
                matches = filter(lambda ct: getattr(ct[1], key) == value,
                    matches)
        if len(matches) == 1:
            return matches[0]
        criteria_string = ', '.join(
            ['%s=%s' % (k, v) for (k, v) in criteria.iteritems()])
        if len(matches) == 0:
            raise LookupError(u'"%s" match no tracks' % criteria_string)
        else:
            raise LookupError(u'"%s" match multiple tracks' % criteria_string)

    def load(self, tracks):
        """
        Replace the tracks in the current playlist with the given tracks.

        :param tracks: tracks to load
        :type tracks: list of :class:`mopidy.models.Track`
        """
        self._cp_tracks = []
        self.version += 1
        for track in tracks:
            self.add(track)
        self.backend.playback.new_playlist_loaded_callback()

    def move(self, start, end, to_position):
        """
        Move the tracks in the slice ``[start:end]`` to ``to_position``.

        :param start: position of first track to move
        :type start: int
        :param end: position after last track to move
        :type end: int
        :param to_position: new position for the tracks
        :type to_position: int
        """
        if start == end:
            end += 1

        cp_tracks = self._cp_tracks

        assert start < end, 'start must be smaller than end'
        assert start >= 0, 'start must be at least zero'
        assert end <= len(cp_tracks), \
            'end can not be larger than playlist length'
        assert to_position >= 0, 'to_position must be at least zero'
        assert to_position <= len(cp_tracks), \
            'to_position can not be larger than playlist length'

        new_cp_tracks = cp_tracks[:start] + cp_tracks[end:]
        for cp_track in cp_tracks[start:end]:
            new_cp_tracks.insert(to_position, cp_track)
            to_position += 1
        self._cp_tracks = new_cp_tracks
        self.version += 1

    def remove(self, **criteria):
        """
        Remove the track from the current playlist.

        Uses :meth:`get()` to lookup the track to remove.

        :param criteria: on or more criteria to match by
        :type criteria: dict
        :type track: :class:`mopidy.models.Track`
        """
        cp_track = self.get(**criteria)
        position = self._cp_tracks.index(cp_track)
        del self._cp_tracks[position]
        self.version += 1

    def shuffle(self, start=None, end=None):
        """
        Shuffles the entire playlist. If ``start`` and ``end`` is given only
        shuffles the slice ``[start:end]``.

        :param start: position of first track to shuffle
        :type start: int or :class:`None`
        :param end: position after last track to shuffle
        :type end: int or :class:`None`
        """
        cp_tracks = self._cp_tracks

        if start is not None and end is not None:
            assert start < end, 'start must be smaller than end'

        if start is not None:
            assert start >= 0, 'start must be at least zero'

        if end is not None:
            assert end <= len(cp_tracks), 'end can not be larger than ' + \
                'playlist length'

        before = cp_tracks[:start or 0]
        shuffled = cp_tracks[start:end]
        after = cp_tracks[end or len(cp_tracks):]
        random.shuffle(shuffled)
        self._cp_tracks = before + shuffled + after
        self.version += 1

    def mpd_format(self, *args, **kwargs):
        """Not a part of the generic backend API."""
        kwargs['cpids'] = [ct[0] for ct in self._cp_tracks]
        return serializer.tracks_to_mpd_format(self.tracks, *args, **kwargs)


class BaseLibraryController(object):
    """
    :param backend: backend the controller is a part of
    :type backend: :class:`BaseBackend`
    """

    def __init__(self, backend):
        self.backend = backend

    def destroy(self):
        """Cleanup after component."""
        pass

    def find_exact(self, field, query):
        """
        Find tracks in the library where ``field`` matches ``query`` exactly.

        :param field: 'track', 'artist', or 'album'
        :type field: string
        :param query: the search query
        :type query: string
        :rtype: :class:`mopidy.models.Playlist`
        """
        raise NotImplementedError

    def lookup(self, uri):
        """
        Lookup track with given URI. Returns :class:`None` if not found.

        :param uri: track URI
        :type uri: string
        :rtype: :class:`mopidy.models.Track` or :class:`None`
        """
        raise NotImplementedError

    def refresh(self, uri=None):
        """
        Refresh library. Limit to URI and below if an URI is given.

        :param uri: directory or track URI
        :type uri: string
        """
        raise NotImplementedError

    def search(self, field, query):
        """
        Search the library for tracks where ``field`` contains ``query``.

        :param field: 'track', 'artist', 'album', 'uri', and 'any'
        :type field: string
        :param query: the search query
        :type query: string
        :rtype: :class:`mopidy.models.Playlist`
        """
        raise NotImplementedError


class BasePlaybackController(object):
    """
    :param backend: backend the controller is a part of
    :type backend: :class:`BaseBackend`
    """

    #: Constant representing the paused state.
    PAUSED = u'paused'

    #: Constant representing the playing state.
    PLAYING = u'playing'

    #: Constant representing the stopped state.
    STOPPED = u'stopped'

    #: :class:`True`
    #:     Tracks are removed from the playlist when they have been played.
    #: :class:`False`
    #:     Tracks are not removed from the playlist.
    consume = False

    #: The currently playing or selected track
    #:
    #: A two-tuple of (CPID integer, :class:`mopidy.models.Track`) or
    #: :class:`None`.
    current_cp_track = None

    #: :class:`True`
    #:     Tracks are selected at random from the playlist.
    #: :class:`False`
    #:     Tracks are played in the order of the playlist.
    random = False

    #: :class:`True`
    #:     The current playlist is played repeatedly. To repeat a single track,
    #:     select both :attr:`repeat` and :attr:`single`.
    #: :class:`False`
    #:     The current playlist is played once.
    repeat = False

    #: :class:`True`
    #:     Playback is stopped after current song, unless in repeat mode.
    #: :class:`False`
    #:     Playback continues after current song.
    single = False

    def __init__(self, backend):
        self.backend = backend
        self._state = self.STOPPED
        self._shuffled = []
        self._first_shuffle = True
        self._play_time_accumulated = 0
        self._play_time_started = None

    def destroy(self):
        """Cleanup after component."""
        pass

    @property
    def current_cpid(self):
        """
        The CPID (current playlist ID) of :attr:`current_track`.

        Read-only. Extracted from :attr:`current_cp_track` for convenience.
        """
        if self.current_cp_track is None:
            return None
        return self.current_cp_track[0]

    @property
    def current_track(self):
        """
        The currently playing or selected :class:`mopidy.models.Track`.

        Read-only. Extracted from :attr:`current_cp_track` for convenience.
        """
        if self.current_cp_track is None:
            return None
        return self.current_cp_track[1]

    @property
    def current_playlist_position(self):
        """The position of the current track in the current playlist."""
        if self.current_cp_track is None:
            return None
        try:
            return self.backend.current_playlist.cp_tracks.index(
                self.current_cp_track)
        except ValueError:
            return None

    @property
    def next_track(self):
        """
        The next track in the playlist.

        A :class:`mopidy.models.Track` extracted from :attr:`next_cp_track` for
        convenience.
        """
        next_cp_track = self.next_cp_track
        if next_cp_track is None:
            return None
        return next_cp_track[1]

    @property
    def next_cp_track(self):
        """
        The next track in the playlist.

        A two-tuple of (CPID integer, :class:`mopidy.models.Track`).

        For normal playback this is the next track in the playlist. If repeat
        is enabled the next track can loop around the playlist. When random is
        enabled this should be a random track, all tracks should be played once
        before the list repeats.
        """
        cp_tracks = self.backend.current_playlist.cp_tracks

        if not cp_tracks:
            return None

        if self.random and not self._shuffled:
            if self.repeat or self._first_shuffle:
                logger.debug('Shuffling tracks')
                self._shuffled = cp_tracks
                random.shuffle(self._shuffled)
                self._first_shuffle = False

        if self._shuffled:
            return self._shuffled[0]

        if self.current_cp_track is None:
            return cp_tracks[0]

        if self.repeat:
            return cp_tracks[
                (self.current_playlist_position + 1) % len(cp_tracks)]

        try:
            return cp_tracks[self.current_playlist_position + 1]
        except IndexError:
            return None

    @property
    def previous_track(self):
        """
        The previous track in the playlist.

        A :class:`mopidy.models.Track` extracted from :attr:`previous_cp_track`
        for convenience.
        """
        previous_cp_track = self.previous_cp_track
        if previous_cp_track is None:
            return None
        return previous_cp_track[1]

    @property
    def previous_cp_track(self):
        """
        The previous track in the playlist.

        A two-tuple of (CPID integer, :class:`mopidy.models.Track`).

        For normal playback this is the previous track in the playlist. If
        random and/or consume is enabled it should return the current track
        instead.
        """
        if self.repeat or self.consume or self.random:
            return self.current_cp_track

        if self.current_cp_track is None or self.current_playlist_position == 0:
            return None

        return self.backend.current_playlist.cp_tracks[
            self.current_playlist_position - 1]

    @property
    def state(self):
        """
        The playback state. Must be :attr:`PLAYING`, :attr:`PAUSED`, or
        :attr:`STOPPED`.

        Possible states and transitions:

        .. digraph:: state_transitions

            "STOPPED" -> "PLAYING" [ label="play" ]
            "PLAYING" -> "STOPPED" [ label="stop" ]
            "PLAYING" -> "PAUSED" [ label="pause" ]
            "PLAYING" -> "PLAYING" [ label="play" ]
            "PAUSED" -> "PLAYING" [ label="resume" ]
            "PAUSED" -> "STOPPED" [ label="stop" ]
        """
        return self._state

    @state.setter
    def state(self, new_state):
        (old_state, self._state) = (self.state, new_state)
        logger.debug(u'Changing state: %s -> %s', old_state, new_state)
        # FIXME _play_time stuff assumes backend does not have a better way of
        # handeling this stuff :/
        if (old_state in (self.PLAYING, self.STOPPED)
                and new_state == self.PLAYING):
            self._play_time_start()
        elif old_state == self.PLAYING and new_state == self.PAUSED:
            self._play_time_pause()
        elif old_state == self.PAUSED and new_state == self.PLAYING:
            self._play_time_resume()

    @property
    def time_position(self):
        """Time position in milliseconds."""
        if self.state == self.PLAYING:
            time_since_started = (self._current_wall_time -
                self._play_time_started)
            return self._play_time_accumulated + time_since_started
        elif self.state == self.PAUSED:
            return self._play_time_accumulated
        elif self.state == self.STOPPED:
            return 0

    def _play_time_start(self):
        self._play_time_accumulated = 0
        self._play_time_started = self._current_wall_time

    def _play_time_pause(self):
        time_since_started = self._current_wall_time - self._play_time_started
        self._play_time_accumulated += time_since_started

    def _play_time_resume(self):
        self._play_time_started = self._current_wall_time

    @property
    def _current_wall_time(self):
        return int(time.time() * 1000)

    def end_of_track_callback(self):
        """
        Tell the playback controller that end of track is reached.

        Typically called by :class:`mopidy.process.CoreProcess` after a message
        from a library thread is received.
        """
        if self.next_cp_track is not None:
            self.next()
        else:
            self.stop()
            self.current_cp_track = None

    def new_playlist_loaded_callback(self):
        """
        Tell the playback controller that a new playlist has been loaded.

        Typically called by :class:`mopidy.process.CoreProcess` after a message
        from a library thread is received.
        """
        self.current_cp_track = None
        self._first_shuffle = True
        self._shuffled = []

        if self.state == self.PLAYING:
            if len(self.backend.current_playlist.tracks) > 0:
                self.play()
            else:
                self.stop()
        elif self.state == self.PAUSED:
            self.stop()

    def next(self):
        """Play the next track."""
        original_cp_track = self.current_cp_track

        if self.state == self.STOPPED:
            return
        elif self.next_cp_track is not None and self._next(self.next_track):
            self.current_cp_track = self.next_cp_track
            self.state = self.PLAYING
        elif self.next_cp_track is None:
            self.stop()
            self.current_cp_track = None

        # FIXME handle in play aswell?
        if self.consume:
            self.backend.current_playlist.remove(cpid=original_cp_track[0])

        if self.random and self.current_cp_track in self._shuffled:
            self._shuffled.remove(self.current_cp_track)

    def _next(self, track):
        return self._play(track)

    def pause(self):
        """Pause playback."""
        if self.state == self.PLAYING and self._pause():
            self.state = self.PAUSED

    def _pause(self):
        raise NotImplementedError

    def play(self, cp_track=None):
        """
        Play the given track or the currently active track.

        :param cp_track: track to play
        :type cp_track: two-tuple (CPID integer, :class:`mopidy.models.Track`)
            or :class:`None`
        """

        if cp_track is not None:
            assert cp_track in self.backend.current_playlist.cp_tracks
        elif not self.current_cp_track:
            cp_track = self.next_cp_track

        if self.state == self.PAUSED and cp_track is None:
            self.resume()
        elif cp_track is not None and self._play(cp_track[1]):
            self.current_cp_track = cp_track
            self.state = self.PLAYING

        # TODO Do something sensible when _play() returns False, like calling
        # next(). Adding this todo instead of just implementing it as I want a
        # test case first.

        if self.random and self.current_cp_track in self._shuffled:
            self._shuffled.remove(self.current_cp_track)

    def _play(self, track):
        raise NotImplementedError

    def previous(self):
        """Play the previous track."""
        if (self.previous_cp_track is not None
                and self.state != self.STOPPED
                and self._previous(self.previous_track)):
            self.current_cp_track = self.previous_cp_track
            self.state = self.PLAYING

    def _previous(self, track):
        return self._play(track)

    def resume(self):
        """If paused, resume playing the current track."""
        if self.state == self.PAUSED and self._resume():
            self.state = self.PLAYING

    def _resume(self):
        raise NotImplementedError

    def seek(self, time_position):
        """
        Seeks to time position given in milliseconds.

        :param time_position: time position in milliseconds
        :type time_position: int
        """
        if self.state == self.STOPPED:
            self.play()
        elif self.state == self.PAUSED:
            self.resume()

        if time_position < 0:
            time_position = 0
        elif self.current_track and time_position > self.current_track.length:
            self.next()
            return

        self._seek(time_position)

    def _seek(self, time_position):
        raise NotImplementedError

    def stop(self):
        """Stop playing."""
        if self.state != self.STOPPED and self._stop():
            self.state = self.STOPPED

    def _stop(self):
        raise NotImplementedError


class BaseStoredPlaylistsController(object):
    """
    :param backend: backend the controller is a part of
    :type backend: :class:`BaseBackend`
    """

    def __init__(self, backend):
        self.backend = backend
        self._playlists = []

    def destroy(self):
        """Cleanup after component."""
        pass

    @property
    def playlists(self):
        """List of :class:`mopidy.models.Playlist`."""
        return copy(self._playlists)

    @playlists.setter
    def playlists(self, playlists):
        self._playlists = playlists

    def create(self, name):
        """
        Create a new playlist.

        :param name: name of the new playlist
        :type name: string
        :rtype: :class:`mopidy.models.Playlist`
        """
        raise NotImplementedError

    def delete(self, playlist):
        """
        Delete playlist.

        :param playlist: the playlist to delete
        :type playlist: :class:`mopidy.models.Playlist`
        """
        raise NotImplementedError

    def get(self, **criteria):
        """
        Get playlist by given criterias from the set of stored playlists.

        Raises :exc:`LookupError` if a unique match is not found.

        Examples::

            get(name='a')            # Returns track with name 'a'
            get(uri='xyz')           # Returns track with URI 'xyz'
            get(name='a', uri='xyz') # Returns track with name 'a' and URI 'xyz'

        :param criteria: on or more criteria to match by
        :type criteria: dict
        :rtype: :class:`mopidy.models.Playlist`
        """
        matches = self._playlists
        for (key, value) in criteria.iteritems():
            matches = filter(lambda p: getattr(p, key) == value, matches)
        if len(matches) == 1:
            return matches[0]
        criteria_string = ', '.join(
            ['%s=%s' % (k, v) for (k, v) in criteria.iteritems()])
        if len(matches) == 0:
            raise LookupError('"%s" match no playlists' % criteria_string)
        else:
            raise LookupError('"%s" match multiple playlists' % criteria_string)

    def lookup(self, uri):
        """
        Lookup playlist with given URI in both the set of stored playlists and
        in any other playlist sources.

        :param uri: playlist URI
        :type uri: string
        :rtype: :class:`mopidy.models.Playlist`
        """
        raise NotImplementedError

    def refresh(self):
        """Refresh stored playlists."""
        raise NotImplementedError

    def rename(self, playlist, new_name):
        """
        Rename playlist.

        :param playlist: the playlist
        :type playlist: :class:`mopidy.models.Playlist`
        :param new_name: the new name
        :type new_name: string
        """
        raise NotImplementedError

    def save(self, playlist):
        """
        Save the playlist to the set of stored playlists.

        :param playlist: the playlist
        :type playlist: :class:`mopidy.models.Playlist`
        """
        raise NotImplementedError

    def search(self, query):
        """
        Search for playlists whose name contains ``query``.

        :param query: query to search for
        :type query: string
        :rtype: list of :class:`mopidy.models.Playlist`
        """
        return filter(lambda p: query in p.name, self._playlists)
