"""The JMA Weather Warning Info integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# This line is crucial for the config flow to be discovered.
from . import config_flow

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JMA Weather Warning Info from a config entry."""
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
