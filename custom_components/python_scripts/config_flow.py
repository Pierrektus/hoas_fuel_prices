from homeassistant import config_entries
from .const import DOMAIN
import voluptuous as vol

def validate_postcodes(postcodes):
    """Validate and convert the postcodes input to a list of integers."""
    try:
        # Entferne Leerzeichen und spalte die Postleitzahlen durch Kommas
        postcode_list = [int(pc.strip()) for pc in postcodes.split(",")]
        return postcode_list
    except ValueError:
        raise vol.Invalid("Postcodes must be a comma-separated list of integers")

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example Config Flow."""

    async def async_step_user(self, info):
        """Handle the user step."""
        if info is not None:
            try:
                # Validierung der Postleitzahlen
                postcodes = validate_postcodes(info["Relevant postcodes"])

                # Speichere die Daten und erstelle die Config Entry
                return self.async_create_entry(
                    title="My Example Integration",  # Titel, der in der UI angezeigt wird
                    data={
                        "api_key": info["API-Key"],  # API-Schlüssel
                        "coord_lat": info["Coordinates Latitude"],
                        "coord_lng" : info["Coordinates Longitude"],
                        "radius": info["Radius"],  # Radius
                        "postcodes": postcodes,  # Liste von Postleitzahlen
                        "mqtt_broker": info["MQTT-Broker IP"],  # MQTT-Broker
                        "mqtt_user": info["MQTT User"],  # MQTT-Benutzer
                        "mqtt_pw": info["MQTT PW"],  # MQTT-Passwort
                    },
                )
            except vol.Invalid as e:
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required("API-Key"): str,
                        vol.Required("Coordinates Latitude"): float,
                        vol.Required("Coordinates Longitude"): float,
                        vol.Required("Radius"): int,
                        vol.Required("Relevant postcodes"): str,
                        vol.Required("MQTT-Broker IP"): str,
                        vol.Required("MQTT User"): str,
                        vol.Required("MQTT PW"): str,
                    }),
                    errors={"Relevant postcodes": str(e)},  # Fehleranzeige in der UI
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("API-Key"): str,
                vol.Required("Coordinates Latitude"): float,
                vol.Required("Coordinates Longitude"): float,
                vol.Required("Radius"): int,
                vol.Required("Relevant postcodes"): str,
                vol.Required("MQTT-Broker IP"): str,
                vol.Required("MQTT User"): str,
                vol.Required("MQTT PW"): str,
            }),
        )