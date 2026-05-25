"""Client for the public EWE WattMonitor API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import API_URL, SET_COOKIE_URL


class EweWattMonitorError(Exception):
    """Base error for EWE WattMonitor API failures."""


class EweWattMonitorNotFoundError(EweWattMonitorError):
    """Raised when the API has no data for a municipality key."""


@dataclass(slots=True)
class EweWattMonitorClient:
    """Small API client around the WattMonitor endpoint."""

    session: ClientSession
    _prepared_municipality_key: str | None = None

    async def async_prepare_municipality(
        self, municipality_key: str, municipality_name: str
    ) -> None:
        """Set the municipality cookie expected by the WattMonitor frontend."""
        if self._prepared_municipality_key == municipality_key:
            return

        payload = {
            "name": municipality_name,
            "municipalityKey": municipality_key,
            "icon": f"/-/media/ewe-kip/inhaltsbilder/wappen/{municipality_key}_wappen.png",
        }

        try:
            async with self.session.post(
                SET_COOKIE_URL,
                json=payload,
                headers={"Accept": "application/json"},
                timeout=20,
            ) as response:
                response.raise_for_status()
        except ClientError as err:
            raise EweWattMonitorError(
                f"Could not prepare WattMonitor municipality cookie: {err}"
            ) from err

        self._prepared_municipality_key = municipality_key

    async def async_get_data(
        self, municipality_key: str, municipality_name: str
    ) -> dict[str, Any]:
        """Return current WattMonitor data for a municipality key."""
        await self.async_prepare_municipality(municipality_key, municipality_name)

        try:
            async with self.session.post(
                API_URL,
                json=municipality_key,
                headers={"Accept": "application/json"},
                timeout=20,
            ) as response:
                response.raise_for_status()
                payload = await response.json()
        except ClientError as err:
            raise EweWattMonitorError(f"Could not fetch WattMonitor data: {err}") from err

        if not isinstance(payload, list) or not payload:
            raise EweWattMonitorNotFoundError(
                f"No WattMonitor data found for municipality key {municipality_key}"
            )

        data = payload[0]
        if not isinstance(data, dict):
            raise EweWattMonitorError("WattMonitor API returned an unexpected payload")

        return data
