"""Sensor platform for JMA Weather Warning Info."""
import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import (
    AREA_URL,
    CONF_AREA_CODE,
    DOMAIN,
    TRANS_WARNING,
    WARNING_URL_FORMAT,
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    area_code = config_entry.data[CONF_AREA_CODE]
    session = async_get_clientsession(hass)
    sensor = JmaWarningSensor(session, area_code, config_entry.entry_id)
    async_add_entities([sensor], True)

class JmaWarningSensor(SensorEntity):
    """Representation of a JMA Weather Warning sensor."""

    def __init__(self, session, area_code, entry_id):
        """Initialize the sensor."""
        self._session = session
        self._area_code = area_code
        self._attr_unique_id = f"{entry_id}_{area_code}"
        self._attr_name = f"JMA Weather Warning {area_code}"
        self._attr_attribution = "Data provided by Japan Meteorological Agency"
        self._area_name = None
        self._warnings = []

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return len(self._warnings)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "area_name": self._area_name,
            "warnings": self._warnings,
            "link": f"https://www.jma.go.jp/bosai/warning/#area_type=class20s&area_code={self._area_code}&lang=ja",
        }

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            # 1. Fetch area information
            async with self._session.get(AREA_URL) as response:
                response.raise_for_status()
                area_data = await response.json()

            class20_info = area_data.get("class20s", {}).get(self._area_code)
            if not class20_info:
                _LOGGER.error("Area code %s not found in JMA area data.", self._area_code)
                return

            self._area_name = class20_info["name"]
            class15s_code = class20_info["parent"]
            class10s_code = area_data["class15s"][class15s_code]["parent"]
            office_code = area_data["class10s"][class10s_code]["parent"]

            # 2. Fetch warning information
            warning_url = WARNING_URL_FORMAT.format(office_code)
            async with self._session.get(warning_url) as response:
                response.raise_for_status()
                warning_info = await response.json()

            # 3. Parse warnings
            warning_codes = []
            for office_warnings in warning_info:
                for class20_item in office_warnings.get("warning", {}).get("class20Items", []):
                    if class20_item.get("areaCode") == self._area_code:
                        for kind in class20_item.get("kinds", []):
                            if kind.get("status") not in ("解除", "発表警報・注意報はなし"):
                                warning_codes.append(kind.get("code"))

            self._warnings = [TRANS_WARNING.get(code, f"不明なコード: {code}") for code in warning_codes]
            if self._area_name and self._attr_name.endswith(self._area_code):
                self._attr_name = f"{self._area_name}の気象警報・注意報"

        except Exception as err:
            _LOGGER.error("Error fetching JMA weather warning data: %s", err)
