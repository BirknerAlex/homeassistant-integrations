"""Services for 1KOMMA5GRAD integration."""

from __future__ import annotations

import datetime as dt
from datetime import datetime
from functools import partial
from typing import Any, Final

import voluptuous as vol

from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from homeassistant.exceptions import ServiceValidationError
from homeassistant.util import dt as dt_util

from .const import DOMAIN

PRICE_SERVICE_NAME = "get_prices"
ATTR_START: Final = "start"
ATTR_END: Final = "end"

SERVICE_SCHEMA: Final = vol.Schema(
    {
        vol.Optional(ATTR_START): str,
        vol.Optional(ATTR_END): str,
    }
)


async def __get_prices(call: ServiceCall, *, hass: HomeAssistant) -> ServiceResponse:
    api_connection = hass.data[DOMAIN]

    start = __get_date(call.data.get(ATTR_START), "start")
    end = __get_date(call.data.get(ATTR_END), "end")

    if start >= end:
        end = start + dt.timedelta(days=1)

    prices: dict[str, Any] = {}

    for system in api_connection.get_systems():
        system_id = system["id"]

        prices = api_connection.get_prices(system_id, start, end)

        price_data = [
            {
                "start_time": starts_at,
                "price": price,
            }
            for starts_at, price in prices.items()
        ]

        selected_data = [
            price
            for price in price_data
            if start <= dt.datetime.fromisoformat(price["start_time"]) < end
        ]
        prices[system_id] = selected_data

    return {"prices": prices}


def __get_date(date_input: str | None, mode: str | None) -> datetime:
    """Get date."""
    if not date_input:
        if mode == "end":
            increment = dt.timedelta(days=1)
        else:
            increment = dt.timedelta()
        return dt_util.start_of_local_day() + increment

    if value := dt_util.parse_datetime(date_input):
        return dt_util.as_local(value)

    raise ServiceValidationError(
        "Invalid datetime provided.",
        translation_domain=DOMAIN,
        translation_key="invalid_date",
        translation_placeholders={
            "date": date_input,
        },
    )


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for 1KOMMA5GRAD integration."""

    hass.services.async_register(
        DOMAIN,
        PRICE_SERVICE_NAME,
        partial(__get_prices, hass=hass),
        schema=SERVICE_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )