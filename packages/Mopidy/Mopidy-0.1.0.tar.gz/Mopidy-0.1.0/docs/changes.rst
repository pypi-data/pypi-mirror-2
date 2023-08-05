*******
Changes
*******

This change log is used to track all major changes to Mopidy.


0.1.0 (2010-08-23)
==================

After three weeks of long nights and sprints we're finally pleased enough with
the state of Mopidy to remove the alpha label, and do a regular release.

Mopidy 0.1.0 got important improvements in search functionality, working track
position seeking, no known stability issues, and greatly improved MPD client
support. There are lots of changes since 0.1.0a3, and we urge you to at least
read the *important changes* below.

This release does not support OS X. We're sorry about that, and are working on
fixing the OS X issues for a future release. You can track the progress at
:issue:`14`.

**Important changes**

- License changed from GPLv2 to Apache License, version 2.0.
- GStreamer is now a required dependency. See our :doc:`GStreamer installation
  docs <installation/gstreamer>`.
- :mod:`mopidy.backends.libspotify` is now the default backend.
  :mod:`mopidy.backends.despotify` is no longer available. This means that you
  need to install the :doc:`dependencies for libspotify
  <installation/libspotify>`.
- If you used :mod:`mopidy.backends.libspotify` previously, pyspotify must be
  updated when updating to this release, to get working seek functionality.
- :attr:`mopidy.settings.SERVER_HOSTNAME` and
  :attr:`mopidy.settings.SERVER_PORT` has been renamed to
  :attr:`mopidy.settings.MPD_SERVER_HOSTNAME` and
  :attr:`mopidy.settings.MPD_SERVER_PORT` to allow for multiple frontends in
  the future.

**Changes**

- Exit early if not Python >= 2.6, < 3.
- Validate settings at startup and print useful error messages if the settings
  has not been updated or anything is misspelled.
- Add command line option :option:`--list-settings` to print the currently
  active settings.
- Include Sphinx scripts for building docs, pylintrc, tests and test data in
  the packages created by ``setup.py`` for i.e. PyPI.
- MPD frontend:

  - Search improvements, including support for multi-word search.
  - Fixed ``play "-1"`` and ``playid "-1"`` behaviour when playlist is empty
    or when a current track is set.
  - Support ``plchanges "-1"`` to work better with MPDroid.
  - Support ``pause`` without arguments to work better with MPDroid.
  - Support ``plchanges``, ``play``, ``consume``, ``random``, ``repeat``, and
    ``single`` without quotes to work better with BitMPC.
  - Fixed deletion of the currently playing track from the current playlist,
    which crashed several clients.
  - Implement ``seek`` and ``seekid``.
  - Fix ``playlistfind`` output so the correct song is played when playing
    songs directly from search results in GMPC.
  - Fix ``load`` so that one can append a playlist to the current playlist, and
    make it return the correct error message if the playlist is not found.
  - Support for single track repeat added. (Fixes: :issue:`4`)
  - Relocate from :mod:`mopidy.mpd` to :mod:`mopidy.frontends.mpd`.
  - Split gigantic protocol implementation into eleven modules.
  - Rename ``mopidy.frontends.mpd.{serializer => translator}`` to match naming
    in backends.
  - Remove setting :attr:`mopidy.settings.SERVER` and
    :attr:`mopidy.settings.FRONTEND` in favour of the new
    :attr:`mopidy.settings.FRONTENDS`.
  - Run MPD server in its own process.

- Backends:

  - Rename :mod:`mopidy.backends.gstreamer` to :mod:`mopidy.backends.local`.
  - Remove :mod:`mopidy.backends.despotify`, as Despotify is little maintained
    and the Libspotify backend is working much better. (Fixes: :issue:`9`,
    :issue:`10`, :issue:`13`)
  - A Spotify application key is now bundled with the source.
    :attr:`mopidy.settings.SPOTIFY_LIB_APPKEY` is thus removed.
  - If failing to play a track, playback will skip to the next track.
  - Both :mod:`mopidy.backends.libspotify` and :mod:`mopidy.backends.local`
    have been rewritten to use the new common GStreamer audio output module,
    :mod:`mopidy.outputs.gstreamer`.

- Mixers:

  - Added new :mod:`mopidy.mixers.gstreamer_software.GStreamerSoftwareMixer`
    which now is the default mixer on all platforms.
  - New setting :attr:`mopidy.settings.MIXER_MAX_VOLUME` for capping the
    maximum output volume.

- Backend API:

  - Relocate from :mod:`mopidy.backends` to :mod:`mopidy.backends.base`.
  - The ``id`` field of :class:`mopidy.models.Track` has been removed, as it is
    no longer needed after the CPID refactoring.
  - :meth:`mopidy.backends.base.BaseBackend()` now accepts an
    ``output_queue`` which it can use to send messages (i.e. audio data)
    to the output process.
  - :meth:`mopidy.backends.base.BaseLibraryController.find_exact()` now accepts
    keyword arguments of the form ``find_exact(artist=['foo'],
    album=['bar'])``.
  - :meth:`mopidy.backends.base.BaseLibraryController.search()` now accepts
    keyword arguments of the form ``search(artist=['foo', 'fighters'],
    album=['bar', 'grooves'])``.
  - :meth:`mopidy.backends.base.BaseCurrentPlaylistController.append()`
    replaces
    :meth:`mopidy.backends.base.BaseCurrentPlaylistController.load()`. Use
    :meth:`mopidy.backends.base.BaseCurrentPlaylistController.clear()` if you
    want to clear the current playlist.
  - The following fields in
    :class:`mopidy.backends.base.BasePlaybackController` has been renamed to
    reflect their relation to methods called on the controller:

    - ``next_track`` to ``track_at_next``
    - ``next_cp_track`` to ``cp_track_at_next``
    - ``previous_track`` to ``track_at_previous``
    - ``previous_cp_track`` to ``cp_track_at_previous``

  - :attr:`mopidy.backends.base.BasePlaybackController.track_at_eot` and
    :attr:`mopidy.backends.base.BasePlaybackController.cp_track_at_eot` has
    been added to better handle the difference between the user pressing next
    and the current track ending.
  - Rename
    :meth:`mopidy.backends.base.BasePlaybackController.new_playlist_loaded_callback()`
    to
    :meth:`mopidy.backends.base.BasePlaybackController.on_current_playlist_change()`.
  - Rename
    :meth:`mopidy.backends.base.BasePlaybackController.end_of_track_callback()`
    to :meth:`mopidy.backends.base.BasePlaybackController.on_end_of_track()`.
  - Remove :meth:`mopidy.backends.base.BaseStoredPlaylistsController.search()`
    since it was barely used, untested, and we got no use case for non-exact
    search in stored playlists yet. Use
    :meth:`mopidy.backends.base.BaseStoredPlaylistsController.get()` instead.


0.1.0a3 (2010-08-03)
====================

In the last two months, Mopidy's MPD frontend has gotten lots of stability
fixes and error handling improvements, proper support for having the same track
multiple times in a playlist, and support for IPv6. We have also fixed the
choppy playback on the libspotify backend. For the road ahead of us, we got an
updated :doc:`release roadmap <development/roadmap>` with our goals for the 0.1
to 0.3 releases.

Enjoy the best alpha relase of Mopidy ever :-)

**Changes**

- MPD frontend:

  - Support IPv6.
  - ``addid`` responds properly on errors instead of crashing.
  - ``commands`` support, which makes RelaXXPlayer work with Mopidy. (Fixes:
    :issue:`6`)
  - Does no longer crash on invalid data, i.e. non-UTF-8 data.
  - ``ACK`` error messages are now MPD-compliant, which should make clients
    handle errors from Mopidy better.
  - Requests to existing commands with wrong arguments are no longer reported
    as unknown commands.
  - ``command_list_end`` before ``command_list_start`` now returns unknown
    command error instead of crashing.
  - ``list`` accepts field argument without quotes and capitalized, to work
    with GMPC and ncmpc.
  - ``noidle`` command now returns ``OK`` instead of an error. Should make some
    clients work a bit better.
  - Having multiple identical tracks in a playlist is now working properly.
    (CPID refactoring)

- Despotify backend:

  - Catch and log :exc:`spytify.SpytifyError`. (Fixes: :issue:`11`)

- Libspotify backend:

  - Fix choppy playback using the Libspotify backend by using blocking ALSA
    mode. (Fixes: :issue:`7`)

- Backend API:

  - A new data structure called ``cp_track`` is now used in the current
    playlist controller and the playback controller. A ``cp_track`` is a
    two-tuple of (CPID integer, :class:`mopidy.models.Track`), identifying an
    instance of a track uniquely within the current playlist.
  - :meth:`mopidy.backends.BaseCurrentPlaylistController.load()` now accepts
    lists of :class:`mopidy.models.Track` instead of
    :class:`mopidy.models.Playlist`, as none of the other fields on the
    ``Playlist`` model was in use.
  - :meth:`mopidy.backends.BaseCurrentPlaylistController.add()` now returns the
    ``cp_track`` added to the current playlist.
  - :meth:`mopidy.backends.BaseCurrentPlaylistController.remove()` now takes
    criterias, just like
    :meth:`mopidy.backends.BaseCurrentPlaylistController.get()`.
  - :meth:`mopidy.backends.BaseCurrentPlaylistController.get()` now returns a
    ``cp_track``.
  - :attr:`mopidy.backends.BaseCurrentPlaylistController.tracks` is now
    read-only. Use the methods to change its contents.
  - :attr:`mopidy.backends.BaseCurrentPlaylistController.cp_tracks` is a
    read-only list of ``cp_track``. Use the methods to change its contents.
  - :attr:`mopidy.backends.BasePlaybackController.current_track` is now
    just for convenience and read-only. To set the current track, assign a
    ``cp_track`` to
    :attr:`mopidy.backends.BasePlaybackController.current_cp_track`.
  - :attr:`mopidy.backends.BasePlaybackController.current_cpid` is the
    read-only CPID of the current track.
  - :attr:`mopidy.backends.BasePlaybackController.next_cp_track` is the
    next ``cp_track`` in the playlist.
  - :attr:`mopidy.backends.BasePlaybackController.previous_cp_track` is
    the previous ``cp_track`` in the playlist.
  - :meth:`mopidy.backends.BasePlaybackController.play()` now takes a
    ``cp_track``.


0.1.0a2 (2010-06-02)
====================

It has been a rather slow month for Mopidy, but we would like to keep up with
the established pace of at least a release per month.

**Changes**

- Improvements to MPD protocol handling, making Mopidy work much better with a
  group of clients, including ncmpc, MPoD, and Theremin.
- New command line flag :option:`--dump` for dumping debug log to ``dump.log``
  in the current directory.
- New setting :attr:`mopidy.settings.MIXER_ALSA_CONTROL` for forcing what ALSA
  control :class:`mopidy.mixers.alsa.AlsaMixer` should use.


0.1.0a1 (2010-05-04)
====================

Since the previous release Mopidy has seen about 300 commits, more than 200 new
tests, a libspotify release, and major feature additions to Spotify. The new
releases from Spotify have lead to updates to our dependencies, and also to new
bugs in Mopidy. Thus, this is primarily a bugfix release, even though the not
yet finished work on a Gstreamer backend have been merged.

All users are recommended to upgrade to 0.1.0a1, and should at the same time
ensure that they have the latest versions of our dependencies: Despotify r508
if you are using DespotifyBackend, and pyspotify 1.1 with libspotify 0.0.4 if
you are using LibspotifyBackend.

As always, report problems at our IRC channel or our issue tracker. Thanks!

**Changes**

- Backend API changes:

  - Removed ``backend.playback.volume`` wrapper. Use ``backend.mixer.volume``
    directly.
  - Renamed ``backend.playback.playlist_position`` to
    ``current_playlist_position`` to match naming of ``current_track``.
  - Replaced ``get_by_id()`` with a more flexible ``get(**criteria)``.

- Merged the ``gstreamer`` branch from Thomas Adamcik:

  - More than 200 new tests, and thus several bugfixes to existing code.
  - Several new generic features, like shuffle, consume, and playlist repeat.
    (Fixes: :issue:`3`)
  - **[Work in Progress]** A new backend for playing music from a local music
    archive using the Gstreamer library.

- Made :class:`mopidy.mixers.alsa.AlsaMixer` work on machines without a mixer
  named "Master".
- Make :class:`mopidy.backends.DespotifyBackend` ignore local files in
  playlists (feature added in Spotify 0.4.3). Reported by Richard Haugen Olsen.
- And much more.


0.1.0a0 (2010-03-27)
====================

"*Release early. Release often. Listen to your customers.*" wrote Eric S.
Raymond in *The Cathedral and the Bazaar*.

Three months of development should be more than enough. We have more to do, but
Mopidy is working and usable. 0.1.0a0 is an alpha release, which basicly means
we will still change APIs, add features, etc. before the final 0.1.0 release.
But the software is usable as is, so we release it. Please give it a try and
give us feedback, either at our IRC channel or through the `issue tracker
<http://github.com/jodal/mopidy/issues>`_. Thanks!

**Changes**

- Initial version. No changelog available.
