from mopidy import settings

class BaseMixer(object):
    """
    :param backend: a backend instance
    :type mixer: :class:`mopidy.backends.base.BaseBackend`

    **Settings:**

    - :attr:`mopidy.settings.MIXER_MAX_VOLUME`
    """

    def __init__(self, backend, *args, **kwargs):
        self.backend = backend
        self.amplification_factor = settings.MIXER_MAX_VOLUME / 100.0

    @property
    def volume(self):
        """
        The audio volume

        Integer in range [0, 100]. :class:`None` if unknown. Values below 0 is
        equal to 0. Values above 100 is equal to 100.
        """
        if self._get_volume() is None:
            return None
        return int(self._get_volume() / self.amplification_factor)

    @volume.setter
    def volume(self, volume):
        volume = int(int(volume) * self.amplification_factor)
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        self._set_volume(volume)

    def destroy(self):
        pass

    def _get_volume(self):
        """
        Return volume as integer in range [0, 100]. :class:`None` if unknown.

        *Must be implemented by subclass.*
        """
        raise NotImplementedError

    def _set_volume(self, volume):
        """
        Set volume as integer in range [0, 100].

        *Must be implemented by subclass.*
        """
        raise NotImplementedError
