import logging
from threading import Lock

from serial import Serial

from mopidy import settings
from mopidy.mixers import BaseMixer

logger = logging.getLogger(u'mopidy.mixers.denon')

class DenonMixer(BaseMixer):
    """
    Mixer for controlling Denon amplifiers and receivers using the RS-232
    protocol.

    The external mixer is the authoritative source for the current volume.
    This allows the user to use his remote control the volume without Mopidy
    cancelling the volume setting.

    **Dependencies**

    - pyserial (python-serial on Debian/Ubuntu)

    **Settings**

    - :attr:`mopidy.settings.MIXER_EXT_PORT` -- Example: ``/dev/ttyUSB0``
    """

    def __init__(self, *args, **kwargs):
        """
        Connects using the serial specifications from Denon's RS-232 Protocol
        specification: 9600bps 8N1.
        """
        super(DenonMixer, self).__init__(*args, **kwargs)
        device = kwargs.get('device', None)
        self._device = device or Serial(port=settings.MIXER_EXT_PORT,
            timeout=0.2)
        self._levels = ['99'] + ["%(#)02d" % {'#': v} for v in range(0, 99)]
        self._volume = 0
        self._lock = Lock()

    def _get_volume(self):
        self._lock.acquire()
        self.ensure_open_device()
        self._device.write('MV?\r')
        vol = str(self._device.readline()[2:4])
        self._lock.release()
        logger.debug(u'_get_volume() = %s' % vol)
        return self._levels.index(vol)

    def _set_volume(self, volume):
        # Clamp according to Denon-spec
        if volume > 99:
            volume = 99
        self._lock.acquire()
        self.ensure_open_device()
        self._device.write('MV%s\r'% self._levels[volume])
        vol = self._device.readline()[2:4]
        self._lock.release()
        self._volume = self._levels.index(vol)

    def ensure_open_device(self):
        if not self._device.isOpen():
            logger.debug(u'(re)connecting to Denon device')
            self._device.open()
