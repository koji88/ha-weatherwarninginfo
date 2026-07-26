"""Config flow for JMA Weather Warning Info integration."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import AREA_URL, CONF_AREA_CODE, DOMAIN

_LOGGER = logging.getLogger(__name__)

class JmaWarningConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JMA Weather Warning Info."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
	"""Handle the initial step."""
	errors = {}
	if user_input is not None:
	    area_code = user_input[CONF_AREA_CODE]
	    try:
		session = async_get_clientsession(self.hass)
		async with session.get(AREA_URL) as response:
		    response.raise_for_status()
		    area_data = await response.json()

		if area_code in area_data.get("class20s", {}):
		    area_name = area_data["class20s"][area_code]["name"]
		    await self.async_set_unique_id(area_code)
		    self._abort_if_unique_id_configured()
		    return self.async_create_entry(
			title=f"{area_name} ({area_code})", data=user_input
		    )
		else:
		    errors["base"] = "invalid_area_code"

	    except Exception:
		_LOGGER.exception("Unexpected exception")
		errors["base"] = "cannot_connect"

	return self.async_show_form(
	    step_id="user",
	    data_schema=vol.Schema({vol.Required(CONF_AREA_CODE): str}),
	    errors=errors,
	)
