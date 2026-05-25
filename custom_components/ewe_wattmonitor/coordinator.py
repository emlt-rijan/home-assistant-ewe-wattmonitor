"""Coordinator for EWE WattMonitor data."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EweWattMonitorClient, EweWattMonitorError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class EweWattMonitorCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch and store current WattMonitor data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: EweWattMonitorClient,
        municipality_key: str,
        municipality_name: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.client = client
        self.municipality_key = municipality_key
        self.municipality_name = municipality_name

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the API."""
        try:
            return await self.client.async_get_data(
                self.municipality_key, self.municipality_name
            )
        except EweWattMonitorError as err:
            raise UpdateFailed(str(err)) from err
