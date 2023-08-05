import logging
import random
import time

logger = logging.getLogger('mopidy.backends.base')

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

    #: The currently playing or selected track.
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
    #:     Playback is stopped after current song, unless in :attr:`repeat`
    #:     mode.
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
        """
        Cleanup after component.

        May be overridden by subclasses.
        """
        pass

    def _get_cpid(self, cp_track):
        if cp_track is None:
            return None
        return cp_track[0]

    def _get_track(self, cp_track):
        if cp_track is None:
            return None
        return cp_track[1]

    @property
    def current_cpid(self):
        """
        The CPID (current playlist ID) of the currently playing or selected
        track.

        Read-only. Extracted from :attr:`current_cp_track` for convenience.
        """
        return self._get_cpid(self.current_cp_track)

    @property
    def current_track(self):
        """
        The currently playing or selected :class:`mopidy.models.Track`.

        Read-only. Extracted from :attr:`current_cp_track` for convenience.
        """
        return self._get_track(self.current_cp_track)

    @property
    def current_playlist_position(self):
        """
        The position of the current track in the current playlist.

        Read-only.
        """
        if self.current_cp_track is None:
            return None
        try:
            return self.backend.current_playlist.cp_tracks.index(
                self.current_cp_track)
        except ValueError:
            return None

    @property
    def track_at_eot(self):
        """
        The track that will be played at the end of the current track.

        Read-only. A :class:`mopidy.models.Track` extracted from
        :attr:`cp_track_at_eot` for convenience.
        """
        return self._get_track(self.cp_track_at_eot)

    @property
    def cp_track_at_eot(self):
        """
        The track that will be played at the end of the current track.

        Read-only. A two-tuple of (CPID integer, :class:`mopidy.models.Track`).

        Not necessarily the same track as :attr:`cp_track_at_next`.
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

        if self.repeat and self.single:
            return cp_tracks[
                (self.current_playlist_position) % len(cp_tracks)]

        if self.repeat:
            return cp_tracks[
                (self.current_playlist_position + 1) % len(cp_tracks)]

        try:
            return cp_tracks[self.current_playlist_position + 1]
        except IndexError:
            return None

    @property
    def track_at_next(self):
        """
        The track that will be played if calling :meth:`next()`.

        Read-only. A :class:`mopidy.models.Track` extracted from
        :attr:`cp_track_at_next` for convenience.
        """
        return self._get_track(self.cp_track_at_next)

    @property
    def cp_track_at_next(self):
        """
        The track that will be played if calling :meth:`next()`.

        Read-only. A two-tuple of (CPID integer, :class:`mopidy.models.Track`).

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
    def track_at_previous(self):
        """
        The track that will be played if calling :meth:`previous()`.

        Read-only. A :class:`mopidy.models.Track` extracted from
        :attr:`cp_track_at_previous` for convenience.
        """
        return self._get_track(self.cp_track_at_previous)

    @property
    def cp_track_at_previous(self):
        """
        The track that will be played if calling :meth:`previous()`.

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

    def on_end_of_track(self):
        """
        Tell the playback controller that end of track is reached.

        Typically called by :class:`mopidy.process.CoreProcess` after a message
        from a library thread is received.
        """
        if self.state == self.STOPPED:
            return

        original_cp_track = self.current_cp_track
        if self.cp_track_at_eot:
            self.play(self.cp_track_at_eot)

            if self.random and self.current_cp_track in self._shuffled:
                self._shuffled.remove(self.current_cp_track)
        else:
            self.stop()
            self.current_cp_track = None

        if self.consume:
            self.backend.current_playlist.remove(cpid=original_cp_track[0])

    def on_current_playlist_change(self):
        """
        Tell the playback controller that the current playlist has changed.

        Used by :class:`mopidy.backends.base.BaseCurrentPlaylistController`.
        """
        self._first_shuffle = True
        self._shuffled = []

        if not self.backend.current_playlist.cp_tracks:
            self.stop()
            self.current_cp_track = None
        elif (self.current_cp_track not in
                self.backend.current_playlist.cp_tracks):
            self.current_cp_track = None
            self.stop()

    def next(self):
        """Play the next track."""
        if self.state == self.STOPPED:
            return

        if self.cp_track_at_next:
            self.play(self.cp_track_at_next)
        else:
            self.stop()
            self.current_cp_track = None

        if self.random and self.current_cp_track in self._shuffled:
            self._shuffled.remove(self.current_cp_track)

    def pause(self):
        """Pause playback."""
        if self.state == self.PLAYING and self._pause():
            self.state = self.PAUSED

    def _pause(self):
        """
        To be overridden by subclass. Implement your backend's pause
        functionality here.

        :rtype: :class:`True` if successful, else :class:`False`
        """
        raise NotImplementedError

    def play(self, cp_track=None, on_error_step=1):
        """
        Play the given track, or if the given track is :class:`None`, play the
        currently active track.

        :param cp_track: track to play
        :type cp_track: two-tuple (CPID integer, :class:`mopidy.models.Track`)
            or :class:`None`
        :param on_error_step: direction to step at play error, 1 for next
            track (default), -1 for previous track
        :type on_error_step: int, -1 or 1
        """

        if cp_track is not None:
            assert cp_track in self.backend.current_playlist.cp_tracks
        elif not self.current_cp_track:
            cp_track = self.cp_track_at_next

        if self.state == self.PAUSED and cp_track is None:
            self.resume()
        elif cp_track is not None:
            self.current_cp_track = cp_track
            self.state = self.PLAYING
            if not self._play(cp_track[1]):
                if on_error_step == 1:
                    self.next()
                elif on_error_step == -1:
                    self.previous()

        if self.random and self.current_cp_track in self._shuffled:
            self._shuffled.remove(self.current_cp_track)

    def _play(self, track):
        """
        To be overridden by subclass. Implement your backend's play
        functionality here.

        :param track: the track to play
        :type track: :class:`mopidy.models.Track`
        :rtype: :class:`True` if successful, else :class:`False`
        """

        raise NotImplementedError

    def previous(self):
        """Play the previous track."""
        if self.cp_track_at_previous is None:
            return
        if self.state == self.STOPPED:
            return
        self.play(self.cp_track_at_previous, on_error_step=-1)

    def resume(self):
        """If paused, resume playing the current track."""
        if self.state == self.PAUSED and self._resume():
            self.state = self.PLAYING

    def _resume(self):
        """
        To be overridden by subclass. Implement your backend's resume
        functionality here.

        :rtype: :class:`True` if successful, else :class:`False`
        """
        raise NotImplementedError

    def seek(self, time_position):
        """
        Seeks to time position given in milliseconds.

        :param time_position: time position in milliseconds
        :type time_position: int
        :rtype: :class:`True` if successful, else :class:`False`
        """
        # FIXME I think return value is only really useful for internal
        # testing, as such it should probably not be exposed in API.
        if self.state == self.STOPPED:
            self.play()
        elif self.state == self.PAUSED:
            self.resume()

        if time_position < 0:
            time_position = 0
        elif self.current_track and time_position > self.current_track.length:
            self.next()
            return

        self._play_time_started = self._current_wall_time
        self._play_time_accumulated = time_position

        return self._seek(time_position)

    def _seek(self, time_position):
        """
        To be overridden by subclass. Implement your backend's seek
        functionality here.

        :param time_position: time position in milliseconds
        :type time_position: int
        :rtype: :class:`True` if successful, else :class:`False`
        """
        raise NotImplementedError

    def stop(self):
        """Stop playing."""
        if self.state != self.STOPPED and self._stop():
            self.state = self.STOPPED

    def _stop(self):
        """
        To be overridden by subclass. Implement your backend's stop
        functionality here.

        :rtype: :class:`True` if successful, else :class:`False`
        """
        raise NotImplementedError
