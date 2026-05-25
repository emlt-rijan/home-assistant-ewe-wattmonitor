"""Config flow for EWE WattMonitor."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from .const import CONF_MUNICIPALITY_KEY, CONF_MUNICIPALITY_NAME, DOMAIN
from .municipalities import (
    load_municipalities,
    municipality_label,
    search_municipality_options,
)

CONF_SEARCH = "search"


class EweWattMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an EWE WattMonitor config flow."""

    VERSION = 1
    _entry_name: str | None = None
    _municipality_options: list[dict[str, str]]

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._entry_name = str(user_input.get(CONF_NAME) or "").strip() or None
            search = str(user_input[CONF_SEARCH]).strip()
            options = await self.hass.async_add_executor_job(
                search_municipality_options, search
            )

            if not options:
                errors[CONF_SEARCH] = "no_results"
            else:
                self._municipality_options = options
                return await self.async_step_select()

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME): str,
                vol.Required(CONF_SEARCH, default="Jork"): str,
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_select(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Select a municipality from filtered search results."""
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

                title = self._entry_name or municipality_label(municipality)
                return self.async_create_entry(
                    title=title,
                    data={
                        CONF_NAME: title,
                        CONF_MUNICIPALITY_KEY: municipality_key,
                        CONF_MUNICIPALITY_NAME: municipality["name"],
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_MUNICIPALITY_KEY,
                    default=self._municipality_options[0]["value"],
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=self._municipality_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
