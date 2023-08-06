**********************
:mod:`mopidy.settings`
**********************


Changing settings
=================

For any Mopidy installation you will need to change at least a couple of
settings. To do this, create a new file in the ``~/.mopidy/`` directory
named ``settings.py`` and add settings you need to change from their defaults
there.

A complete ``~/.mopidy/settings.py`` may look like this::

    MPD_SERVER_HOSTNAME = u'::'
    SPOTIFY_USERNAME = u'alice'
    SPOTIFY_PASSWORD = u'mysecret'


Available settings
==================

.. automodule:: mopidy.settings
    :synopsis: Available settings and their default values
    :members:
    :undoc-members:
