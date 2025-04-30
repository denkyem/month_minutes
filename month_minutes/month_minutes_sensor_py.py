"""Sensor component for Month Minutes."""
from datetime import datetime, timedelta
import calendar
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import TIME_MINUTES
import homeassistant.helpers.config_validation as cv
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

DOMAIN = "month_minutes"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Month Minutes sensors."""
    sensors = [
        MonthMinutesSinceDayOneSensor(),
        MonthTotalMinutesSensor()
    ]
    
    async_add_entities(sensors, True)
    return True

class MonthMinutesSinceDayOneSensor(SensorEntity):
    """Representation of a Sensor that calculates minutes since day 1 of current month."""

    def __init__(self):
        """Initialize the sensor."""
        self._name = "Minutes Since Month Start"
        self._state = None
        self._attr_unique_id = "minutes_since_month_start"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_unit_of_measurement = TIME_MINUTES

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        now = dt_util.now()
        first_day = datetime(now.year, now.month, 1, 0, 0, 0, tzinfo=now.tzinfo)
        delta = now - first_day
        
        # Convert to minutes
        minutes = int(delta.total_seconds() / 60)
        self._state = minutes

class MonthTotalMinutesSensor(SensorEntity):
    """Representation of a Sensor that calculates total minutes in the current month."""

    def __init__(self):
        """Initialize the sensor."""
        self._name = "Total Minutes In Month"
        self._state = None
        self._attr_unique_id = "total_minutes_in_month"
        self._attr_icon = "mdi:calendar-month"
        self._attr_unit_of_measurement = TIME_MINUTES

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        now = dt_util.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        
        # Calculate total minutes in the month
        total_minutes = days_in_month * 24 * 60
        self._state = total_minutes
