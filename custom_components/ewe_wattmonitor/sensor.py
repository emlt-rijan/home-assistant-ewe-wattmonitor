"""Sensors for EWE WattMonitor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, PERCENTAGE, UnitOfPower, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_LAST_UPDATE,
    ATTR_MUNICIPALITY_KEY,
    ATTR_MUNICIPALITY_NAME,
    ATTRIBUTION,
    CONF_MUNICIPALITY_KEY,
    CONF_MUNICIPALITY_NAME,
    DOMAIN,
)
from .coordinator import EweWattMonitorCoordinator

PARALLEL_UPDATES = 0


def _value(key: str) -> Callable[[dict[str, Any]], float | int | str | None]:
    def getter(data: dict[str, Any]) -> float | int | str | None:
        return data.get(key)

    return getter


def _balance(data: dict[str, Any]) -> float | int | None:
    generation = data.get("ErzeugungSumme")
    consumption = data.get("VerbrauchSumme")
    if generation is None or consumption is None:
        return None
    return generation - consumption


def _renewable_percentage(data: dict[str, Any]) -> float | None:
    generation = data.get("ErzeugungSumme")
    consumption = data.get("VerbrauchSumme")
    if not generation or not consumption:
        return None
    return round(generation / consumption * 100, 2)


@dataclass(frozen=True, kw_only=True)
class EweWattMonitorSensorEntityDescription(SensorEntityDescription):
    """Describes an EWE WattMonitor sensor."""

    value_fn: Callable[[dict[str, Any]], float | int | str | None]


SENSORS: tuple[EweWattMonitorSensorEntityDescription, ...] = (
    EweWattMonitorSensorEntityDescription(
        key="consumption",
        translation_key="consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("VerbrauchSumme"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="generation",
        translation_key="generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("ErzeugungSumme"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="balance",
        translation_key="balance",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_balance,
    ),
    EweWattMonitorSensorEntityDescription(
        key="solar_generation",
        translation_key="solar_generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("ErzeugungPv"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="wind_generation",
        translation_key="wind_generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("ErzeugungWind"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="biomass_generation",
        translation_key="biomass_generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("ErzeugungBiomasse"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="hydro_generation",
        translation_key="hydro_generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("ErzeugungWasser"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="other_generation",
        translation_key="other_generation",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("ErzeugungSonstige"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="renewable_percentage",
        translation_key="renewable_percentage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_renewable_percentage,
    ),
    EweWattMonitorSensorEntityDescription(
        key="temperature",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("Temperatur"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="wind_speed",
        translation_key="wind_speed",
        native_unit_of_measurement="m/s",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("Windstaerke"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="wind_direction",
        translation_key="wind_direction",
        native_unit_of_measurement="°",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("Windrichtung"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="cloud_coverage",
        translation_key="cloud_coverage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("Bedeckungsgrad"),
    ),
    EweWattMonitorSensorEntityDescription(
        key="precipitation",
        translation_key="precipitation",
        native_unit_of_measurement="mm",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_value("Niederschlag"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EWE WattMonitor sensors."""
    coordinator: EweWattMonitorCoordinator = entry.runtime_data
    async_add_entities(
        EweWattMonitorSensor(coordinator, entry, description) for description in SENSORS
    )


class EweWattMonitorSensor(CoordinatorEntity[EweWattMonitorCoordinator], SensorEntity):
    """Representation of an EWE WattMonitor sensor."""

    _attr_attribution = ATTRIBUTION
    entity_description: EweWattMonitorSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EweWattMonitorCoordinator,
        entry: ConfigEntry,
        description: EweWattMonitorSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry
        self._attr_unique_id = f"{entry.data[CONF_MUNICIPALITY_KEY]}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data[CONF_MUNICIPALITY_KEY])},
            "name": entry.data.get(CONF_NAME),
            "manufacturer": "EWE NETZ",
            "model": "WattMonitor",
            "configuration_url": "https://wattmonitor.ewe-netz.de/",
        }

    @property
    def native_value(self) -> float | int | str | None:
        """Return the sensor value."""
        if not self.coordinator.data:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return metadata shared by all sensors."""
        return {
            ATTR_MUNICIPALITY_KEY: self._entry.data[CONF_MUNICIPALITY_KEY],
            ATTR_MUNICIPALITY_NAME: self._entry.data.get(CONF_MUNICIPALITY_NAME),
            ATTR_LAST_UPDATE: self.coordinator.data.get("Zeitpunkt")
            if self.coordinator.data
            else None,
        }
