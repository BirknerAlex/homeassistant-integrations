"""Adds config flow for 1KOMMA5GRAD integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components.ios import CONF_USER

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

from .api.error import TokenError
from .const import DOMAIN
from .api.client import Client

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str
})

ERR_TIMEOUT = "timeout"
ERR_CLIENT = "cannot_connect"
ERR_TOKEN = "invalid_access_token"


class HeartbeatConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for 1KOMMA5GRAD integration."""

    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        self._async_abort_entries_match()

        if user_input is not None:
            username = user_input[CONF_USER].replace(" ", "")
            password = user_input[CONF_PASSWORD].replace(" ", "")

            api_connection = Client(
                username=username,
                password=password,
            )

            errors = {}

            try:
                await api_connection.get_token()
            except TokenError:
                errors[CONF_USERNAME] = ERR_TOKEN
                errors[CONF_PASSWORD] = ERR_TOKEN

            if errors:
                return self.async_show_form(
                    step_id="user",
                    data_schema=DATA_SCHEMA,
                    errors=errors,
                )

            user = api_connection.get_user()
            await self.async_set_unique_id(user["id"])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user.email,
                data={
                    CONF_USERNAME: username,
                    CONF_PASSWORD: password,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors={},
        )