import logging
import requests

import voluptuous as vol

from homeassistant.components.cover import (
    CoverDevice, PLATFORM_SCHEMA, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_STOP)
from homeassistant.const import (
    CONF_IP_ADDRESS, CONF_ID, CONF_CODE, CONF_NAME, CONF_COVERS, CONF_DEVICE, STATE_CLOSED, STATE_OPEN, STATE_UNKNOWN)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "morning_rod"
DEFAULT_NAME = 'morning_rod'

CONF_DEVICE_ID = 'device_id'

STATE_CLOSING = 'closing'
STATE_OFFLINE = 'offline'
STATE_OPENING = 'opening'
STATE_STOPPED = 'stopped'

COVER_SCHEMA = vol.Schema({
#     vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
#     vol.Required(CONF_ID): cv.string,
    vol.Required(CONF_CODE): cv.string
})

blindClose = 'http://morningrod.blynk.cc/{}/update/V13?value=1'
blindOpen = 'http://morningrod.blynk.cc/{}/update/V12?value=1'
blindConnectd = 'http://morningrod.blynk.cc/{}/isHardwareConnected'

############

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_COVERS): vol.Schema({cv.slug: COVER_SCHEMA}),
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the neocontroller covers."""
    covers = []
    devices = config.get(CONF_COVERS)

    for device_id, device_config in devices.items():
        args = {
#             CONF_ID: device_config.get(CONF_ID),
            CONF_CODE: device_config.get(CONF_CODE),
            CONF_NAME: device_config.get(CONF_NAME),
#             CONF_DEVICE_ID: device_config.get(CONF_DEVICE, device_id),
        }

        covers.append(MorningRod(hass, args))

    add_devices(covers, True)


class MorningRod(CoverDevice):
    """Representation of MorningRod cover."""

    # pylint: disable=no-self-use
    def __init__(self, hass, args):
        """Initialize the cover."""
        self.hass = hass
        self._name = args[CONF_NAME]
#         self.device_id = args['device_id']
#         self._id      = args[CONF_ID]
        self._code    = args[CONF_CODE]
        self._available = False
        self._state = None

    @property
    def name(self):
        """Return the name of the cover."""
        return self._name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available
        
################

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        if self._state in [STATE_UNKNOWN, STATE_OFFLINE]:
            return None
        return self._state in [STATE_CLOSED, STATE_OPENING]

    def update(self):
        """Poll the current state of the device."""
        response = requests.get(blindConnectd.format(self._code))
        if response.status_code == 200:
            if 'true' in response.text:
                self._available = True
            else:
                self._available = False
        else:
            self._available = False

    
    def close_cover(self):
        """Close the cover."""
        requests.get(blindClose.format(self._code))

    def open_cover(self):
        """Open the cover."""
        requests.get(blindOpen.format(self._code))
        
    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return 'curtain'

    @property
    def supported_features(self):
        """Flag supported features."""
        # return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP
        return SUPPORT_OPEN | SUPPORT_CLOSE
