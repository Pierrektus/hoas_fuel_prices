import json
import paho.mqtt.client as mqtt
import logging
import requests
from time import sleep
import re


# TODO : get data from ui conig ?!
# set main data
import mySecrets
api_key = mySecrets.api_key
lat_coords = mySecrets.lat_coords
lng_coords = mySecrets.lng_coords
radius = mySecrets.radius
relevant_postcodes = mySecrets.relevant_postcodes
fuel_types = ['e5', 'e10', 'diesel']
broker_ip = mySecrets.broker_ip
broker_user = mySecrets.broker_user
broker_pw = mySecrets.broker_pw

def state_topic(station_name : str, fuel_type : str) -> str:
    return f"homeassistant/sensor/fuel_prices/{station_name + "_" + fuel_type}/state"

def discover_topic(station_name : str, fuel_type : str) -> str:
    return json.dumps({
    "name": station_name,
    "state_topic": f"homeassistant/sensor/fuel_prices/{station_name + "_" + fuel_type}/state",
    "unit_of_measurement": "€",
    "value_template": "{{ value_json.value }}",
    "device": {
        "identifiers": [
        "fuel_prices"
        ],
        "name": "fuel_prices",
        "manufacturer": "Custom",
        "model": "Fuel price monitor",
        "sw_version": "1.0"
    },
    "unique_id": f"{station_name}_{fuel_type}",
    "device_class": "monetary"
    })

api_call = f"https://creativecommons.tankerkoenig.de/json/list.php?lat={lat_coords}&lng={lng_coords}&rad={radius}&sort=dist&type=all&apikey={api_key}"
response = requests.get(api_call)
response.encoding = 'utf-8'
contents = response.json()

# TODO : DELETE AFTER TESTING
# with open('D:\Programmierung\tank_contents.md','r') as file:
#     contents = json.loads(file.read())

def state_topic_value(fuel_price : float) -> str:
    return json.dumps({"value" : fuel_price})

def on_connect(client, userdata, flags, reason_code, properties=None):
    print('Connected  to broker with reason code', reason_code)

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(username=broker_user, password=broker_pw)
client.connect(host=broker_ip, port=1883, keepalive=60)

client.loop_start()

for station in contents.get('stations'):
    # check if station is in wanted postcode
    if station.get('postCode') in relevant_postcodes:
        # send discover topic once
        # discover_topic(station_name=str(postcode) + "_" + station_name)
        postcode = station.get('postCode')
        station_name = station.get('name')
        sensor_station_name = re.sub(r"[^a-zA-Z0-9_]", "_", str(postcode) + "_" + station_name.replace(" ", "_"))

        for fuel_type in fuel_types:
            client.publish(f"homeassistant/sensor/fuel_prices/{sensor_station_name + "_" + fuel_type}/config", discover_topic(sensor_station_name, fuel_type), 1 , True)
            client.publish(state_topic(sensor_station_name, fuel_type), state_topic_value(station.get(fuel_type)), 1,True)

client.loop_stop()
client.disconnect()