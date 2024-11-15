"""Support for 1KOMMA5GRAD."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import Event, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .api.error import ApiError
from .const import DATA_HASS_CONFIG, DOMAIN, LOGGER_NAME
from .service import async_setup_services

from .api.client import Client

PLATFORMS = [Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER = logging.getLogger(LOGGER_NAME)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the 1KOMMA5GRAD component."""
    hass.data[DATA_HASS_CONFIG] = config

    async_setup_services(hass)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""

    api_connection =  Client(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
    )
    hass.data[DOMAIN] = api_connection

    async def _close(event: Event) -> None:
        await api_connection.close()

    entry.async_on_unload(hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _close))

    try:
        await api_connection.get_user()
    except (
            TimeoutError,
    ) as err:
        raise ConfigEntryNotReady("Unable to connect") from err
    except ApiError as exp:
        _LOGGER.error("Failed API request. %s", exp)
        return False

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
