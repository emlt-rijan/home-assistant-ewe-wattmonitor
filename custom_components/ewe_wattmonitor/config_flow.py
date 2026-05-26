"""Config flow for EWE WattMonitor."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector

from .api import (
    EweWattMonitorClient,
    EweWattMonitorError,
    EweWattMonitorNotFoundError,
)
from .const import CONF_MUNICIPALITY_KEY, CONF_MUNICIPALITY_NAME, DOMAIN
from .municipalities import (
    load_municipalities,
    municipality_options,
)

_LOGGER = logging.getLogger(__name__)


class EweWattMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an EWE WattMonitor config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Select and validate a municipality."""
        errors: dict[str, str] = {}

        if user_input is not None:
            municipality_key = str(user_input[CONF_MUNICIPALITY_KEY]).strip()
            municipalities = await self.hass.async_add_executor_job(load_municipalities)
            municipality = municipalities.get(municipality_key)

            if municipality is None:
                errors[CONF_MUNICIPALITY_KEY] = "unsupported_municipality"
            else:
                await self.async_set_unique_id(municipality_key)
                self._abort_if_unique_id_configured()

                client = EweWattMonitorClient(async_get_clientsession(self.hass))
                try:
                    await client.async_get_data(municipality_key, municipality["name"])
                except EweWattMonitorNotFoundError:
                    errors[CONF_MUNICIPALITY_KEY] = "not_found"
                except EweWattMonitorError:
                    errors[CONF_MUNICIPALITY_KEY] = "cannot_connect"
                except Exception:  # noqa: BLE001
                    _LOGGER.exception("Unexpected exception validating municipality")
                    errors[CONF_MUNICIPALITY_KEY] = "unknown"
                else:
                    return await self._async_create_municipality_entry(
                        municipality_key,
                        municipality,
                    )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_MUNICIPALITY_KEY,
                    default="03359028",
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=await self.hass.async_add_executor_job(
                            municipality_options
                        ),
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )
        return self.async_show_form(
            step_id="select",
            data_schema=data_schema,
            errors=errors,
        )

    async def _async_create_municipality_entry(
        self,
        municipality_key: str,
        municipality: dict[str, str],
    ) -> config_entries.FlowResult:
        """Create the config entry for a selected municipality."""
        title = municipality["name"]
        return self.async_create_entry(
            title=title,
            data={
                CONF_NAME: title,
                CONF_MUNICIPALITY_KEY: municipality_key,
                CONF_MUNICIPALITY_NAME: municipality["name"],
            },
        )
