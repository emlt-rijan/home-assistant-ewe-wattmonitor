"""The EWE WattMonitor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import EweWattMonitorClient
from .const import CONF_MUNICIPALITY_KEY, CONF_MUNICIPALITY_NAME
from .coordinator import EweWattMonitorCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EWE WattMonitor from a config entry."""
    client = EweWattMonitorClient(async_get_clientsession(hass))
    coordinator = EweWattMonitorCoordinator(
        hass,
        client,
        entry.data[CONF_MUNICIPALITY_KEY],
        entry.data[CONF_MUNICIPALITY_NAME],
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
