import glob
import logging
import multiprocessing
import os
import shutil

from mopidy import settings
from mopidy.backends.base import *
from mopidy.models import Playlist, Track, Album
from mopidy.utils.process import pickle_connection

from .translator import parse_m3u, parse_mpd_tag_cache

logger = logging.getLogger(u'mopidy.backends.local')

class LocalBackend(BaseBackend):
    """
    A backend for playing music from a local music archive.

    **Issues:** http://github.com/jodal/mopidy/issues/labels/backend-local

    **Settings:**

    - :attr:`mopidy.settings.LOCAL_MUSIC_FOLDER`
    - :attr:`mopidy.settings.LOCAL_PLAYLIST_FOLDER`
    - :attr:`mopidy.settings.LOCAL_TAG_CACHE`
    """

    def __init__(self, *args, **kwargs):
        super(LocalBackend, self).__init__(*args, **kwargs)

        self.library = LocalLibraryController(self)
        self.stored_playlists = LocalStoredPlaylistsController(self)
        self.current_playlist = BaseCurrentPlaylistController(self)
        self.playback = LocalPlaybackController(self)
        self.uri_handlers = [u'file://']


class LocalPlaybackController(BasePlaybackController):
    def __init__(self, backend):
        super(LocalPlaybackController, self).__init__(backend)
        self.stop()

    def _play(self, track):
        return self.backend.output.play_uri(track.uri)

    def _stop(self):
        return self.backend.output.set_state('READY')

    def _pause(self):
        return self.backend.output.set_state('PAUSED')

    def _resume(self):
        return self.backend.output.set_state('PLAYING')

    def _seek(self, time_position):
        return self.backend.output.set_position(time_position)

    @property
    def time_position(self):
        return self.backend.output.get_position()


class LocalStoredPlaylistsController(BaseStoredPlaylistsController):
    def __init__(self, *args):
        super(LocalStoredPlaylistsController, self).__init__(*args)
        self._folder = os.path.expanduser(settings.LOCAL_PLAYLIST_FOLDER)
        self.refresh()

    def lookup(self, uri):
        pass # TODO

    def refresh(self):
        playlists = []

        logger.info('Loading playlists from %s', self._folder)

        for m3u in glob.glob(os.path.join(self._folder, '*.m3u')):
            name = os.path.basename(m3u)[:len('.m3u')]
            tracks = []
            for uri in parse_m3u(m3u):
                try:
                    tracks.append(self.backend.library.lookup(uri))
                except LookupError, e:
                    logger.error('Playlist item could not be added: %s', e)
            playlist = Playlist(tracks=tracks, name=name)

            # FIXME playlist name needs better handling
            # FIXME tracks should come from lib. lookup

            playlists.append(playlist)

        self.playlists = playlists

    def create(self, name):
        playlist = Playlist(name=name)
        self.save(playlist)
        return playlist

    def delete(self, playlist):
        if playlist not in self._playlists:
            return

        self._playlists.remove(playlist)
        filename = os.path.join(self._folder, playlist.name + '.m3u')

        if os.path.exists(filename):
            os.remove(filename)

    def rename(self, playlist, name):
        if playlist not in self._playlists:
            return

        src = os.path.join(self._folder, playlist.name + '.m3u')
        dst = os.path.join(self._folder, name + '.m3u')

        renamed = playlist.with_(name=name)
        index = self._playlists.index(playlist)
        self._playlists[index] = renamed

        shutil.move(src, dst)

    def save(self, playlist):
        file_path = os.path.join(self._folder, playlist.name + '.m3u')

        # FIXME this should be a save_m3u function, not inside save
        with open(file_path, 'w') as file_handle:
            for track in playlist.tracks:
                if track.uri.startswith('file://'):
                    file_handle.write(track.uri[len('file://'):] + '\n')
                else:
                    file_handle.write(track.uri + '\n')

        self._playlists.append(playlist)


class LocalLibraryController(BaseLibraryController):
    def __init__(self, backend):
        super(LocalLibraryController, self).__init__(backend)
        self._uri_mapping = {}
        self.refresh()

    def refresh(self, uri=None):
        tracks = parse_mpd_tag_cache(settings.LOCAL_TAG_CACHE,
            settings.LOCAL_MUSIC_FOLDER)

        logger.info('Loading songs in %s from %s',
            settings.LOCAL_MUSIC_FOLDER, settings.LOCAL_TAG_CACHE)

        for track in tracks:
            self._uri_mapping[track.uri] = track

    def lookup(self, uri):
        try:
            return self._uri_mapping[uri]
        except KeyError:
            raise LookupError('%s not found.' % uri)

    def find_exact(self, **query):
        self._validate_query(query)
        result_tracks = self._uri_mapping.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip()

                track_filter = lambda t: q == t.name
                album_filter = lambda t: q == getattr(t, 'album', Album()).name
                artist_filter = lambda t: filter(
                    lambda a: q == a.name, t.artists)
                uri_filter = lambda t: q == t.uri
                any_filter = lambda t: (track_filter(t) or album_filter(t) or
                    artist_filter(t) or uri_filter(t))

                if field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field == 'uri':
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)
        return Playlist(tracks=result_tracks)

    def search(self, **query):
        self._validate_query(query)
        result_tracks = self._uri_mapping.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip().lower()

                track_filter  = lambda t: q in t.name.lower()
                album_filter = lambda t: q in getattr(
                    t, 'album', Album()).name.lower()
                artist_filter = lambda t: filter(
                    lambda a: q in a.name.lower(), t.artists)
                uri_filter = lambda t: q in t.uri.lower()
                any_filter = lambda t: track_filter(t) or album_filter(t) or \
                    artist_filter(t) or uri_filter(t)

                if field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field == 'uri':
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)
        return Playlist(tracks=result_tracks)

    def _validate_query(self, query):
        for (_, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')
