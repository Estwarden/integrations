"""EstWarden threat level sensor."""
import logging
from datetime import timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=15)
API = "https://estwarden.eu"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    session = async_get_clientsession(hass)
    async_add_entities([
        EstWardenThreatLevel(session),
        EstWardenThreatScore(session),
    ], True)

class EstWardenThreatLevel(SensorEntity):
    _attr_name = "Baltic Threat Level"
    _attr_unique_id = "estwarden_threat_level"
    _attr_icon = "mdi:shield-alert"

    def __init__(self, session):
        self._session = session
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        try:
            async with self._session.get(f"{API}/api/threat-index") as r:
                data = await r.json()
                self._attr_native_value = data.get("level", "UNKNOWN")
                self._attr_extra_state_attributes = {
                    "score": data.get("score", 0),
                    "date": data.get("date", ""),
                }
        except Exception as e:
            _LOGGER.error("EstWarden API error: %s", e)

class EstWardenThreatScore(SensorEntity):
    _attr_name = "Baltic Threat Score"
    _attr_unique_id = "estwarden_threat_score"
    _attr_native_unit_of_measurement = "/100"
    _attr_icon = "mdi:gauge"

    def __init__(self, session):
        self._session = session
        self._attr_native_value = None

    async def async_update(self):
        try:
            async with self._session.get(f"{API}/api/threat-index") as r:
                data = await r.json()
                self._attr_native_value = round(data.get("score", 0), 1)
        except Exception as e:
            _LOGGER.error("EstWarden API error: %s", e)
