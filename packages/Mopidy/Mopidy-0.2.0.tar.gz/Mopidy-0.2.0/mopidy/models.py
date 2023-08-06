from copy import copy

from mopidy.frontends.mpd import translator

class ImmutableObject(object):
    """
    Superclass for immutable objects whose fields can only be modified via the
    constructor.

    :param kwargs: kwargs to set as fields on the object
    :type kwargs: any
    """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError('__init__() got an unexpected keyword ' + \
                    'argument \'%s\'' % key)
            self.__dict__[key] = value

    def __setattr__(self, name, value):
        if name.startswith('_'):
            return super(ImmutableObject, self).__setattr__(name, value)
        raise AttributeError('Object is immutable.')

    def __hash__(self):
        hash_sum = 0
        for key, value in self.__dict__.items():
            hash_sum += hash(key) + hash(value)
        return hash_sum

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class Artist(ImmutableObject):
    """
    :param uri: artist URI
    :type uri: string
    :param name: artist name
    :type name: string
    """

    #: The artist URI. Read-only.
    uri = None

    #: The artist name. Read-only.
    name = None


class Album(ImmutableObject):
    """
    :param uri: album URI
    :type uri: string
    :param name: album name
    :type name: string
    :param artists: album artists
    :type artists: list of :class:`Artist`
    :param num_tracks: number of tracks in album
    :type num_tracks: integer
    """

    #: The album URI. Read-only.
    uri = None

    #: The album name. Read-only.
    name = None

    #: The number of tracks in the album. Read-only.
    num_tracks = 0

    def __init__(self, *args, **kwargs):
        self._artists = frozenset(kwargs.pop('artists', []))
        super(Album, self).__init__(*args, **kwargs)

    @property
    def artists(self):
        """List of :class:`Artist` elements. Read-only."""
        return list(self._artists)


class Track(ImmutableObject):
    """
    :param uri: track URI
    :type uri: string
    :param name: track name
    :type name: string
    :param artists: track artists
    :type artists: list of :class:`Artist`
    :param album: track album
    :type album: :class:`Album`
    :param track_no: track number in album
    :type track_no: integer
    :param date: track release date
    :type date: :class:`datetime.date`
    :param length: track length in milliseconds
    :type length: integer
    :param bitrate: bitrate in kbit/s
    :type bitrate: integer
    """

    #: The track URI. Read-only.
    uri = None

    #: The track name. Read-only.
    name = None

    #: The track :class:`Album`. Read-only.
    album = None

    #: The track number in album. Read-only.
    track_no = 0

    #: The track release date. Read-only.
    date = None

    #: The track length in milliseconds. Read-only.
    length = None

    #: The track's bitrate in kbit/s. Read-only.
    bitrate = None

    def __init__(self, *args, **kwargs):
        self._artists = frozenset(kwargs.pop('artists', []))
        super(Track, self).__init__(*args, **kwargs)

    @property
    def artists(self):
        """List of :class:`Artist`. Read-only."""
        return list(self._artists)

    def mpd_format(self, *args, **kwargs):
        return translator.track_to_mpd_format(self, *args, **kwargs)


class Playlist(ImmutableObject):
    """
        :param uri: playlist URI
        :type uri: string
        :param name: playlist name
        :type name: string
        :param tracks: playlist's tracks
        :type tracks: list of :class:`Track` elements
        :param last_modified: playlist's modification time
        :type last_modified: :class:`datetime.datetime`
    """

    #: The playlist URI. Read-only.
    uri = None

    #: The playlist name. Read-only.
    name = None

    #: The playlist modification time. Read-only.
    #:
    #: :class:`datetime.datetime`, or :class:`None` if unknown.
    last_modified = None

    def __init__(self, *args, **kwargs):
        self._tracks = kwargs.pop('tracks', [])
        super(Playlist, self).__init__(*args, **kwargs)

    @property
    def tracks(self):
        """List of :class:`Track` elements. Read-only."""
        return copy(self._tracks)

    @property
    def length(self):
        """The number of tracks in the playlist. Read-only."""
        return len(self._tracks)

    def mpd_format(self, *args, **kwargs):
        return translator.playlist_to_mpd_format(self, *args, **kwargs)

    def with_(self, uri=None, name=None, tracks=None, last_modified=None):
        """
        Create a new playlist object with the given values. The values that are
        not given are taken from the object the method is called on.

        Does not change the object on which it is called.

        :param uri: playlist URI
        :type uri: string
        :param name: playlist name
        :type name: string
        :param tracks: playlist's tracks
        :type tracks: list of :class:`Track` elements
        :param last_modified: playlist's modification time
        :type last_modified: :class:`datetime.datetime`
        :rtype: :class:`Playlist`
        """
        if uri is None:
            uri = self.uri
        if name is None:
            name = self.name
        if tracks is None:
            tracks = self.tracks
        if last_modified is None:
            last_modified = self.last_modified
        return Playlist(uri=uri, name=name, tracks=tracks,
            last_modified=last_modified)
