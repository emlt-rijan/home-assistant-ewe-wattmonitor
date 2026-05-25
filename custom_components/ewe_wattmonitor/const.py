"""Constants for the EWE WattMonitor integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "ewe_wattmonitor"
API_URL = "https://wattmonitor.ewe-netz.de/api/getdata"
SET_COOKIE_URL = "https://wattmonitor.ewe-netz.de/api/setcookie"
DEFAULT_SCAN_INTERVAL = timedelta(minutes=15)
ATTRIBUTION = "Data provided by EWE NETZ WattMonitor"

CONF_MUNICIPALITY_KEY = "municipality_key"
CONF_MUNICIPALITY_NAME = "municipality_name"

ATTR_LAST_UPDATE = "last_update"
ATTR_MUNICIPALITY_KEY = "municipality_key"
ATTR_MUNICIPALITY_NAME = "municipality_name"
