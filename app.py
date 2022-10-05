from typing import List

from flask import Flask, render_template, request
from zeep import Client

from services import MapboxDirection, MapboxPlace, ChargingStation, ChargeTrip
from settings import Config
import requests
import datetime

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def build_json_waypoint_markers(waypoints):
    waypoints_data = []
    for waypoint in waypoints:
        waypoint_data = {
            "name": "naaamme",
            "coordinates": [
                waypoint[0],
                waypoint[1]
            ],
            "infos": "Additionnals informations"
        }
        waypoints_data.append(waypoint_data)
    return waypoints_data


def retrieve_total_travel_time(number_stop: int, driving_time: int, charging_time: int):
    client = Client(f"{Config.MAPBOX_ACCESS_KEY}/?wsdl")
    time = client.service.travel_time(int(number_stop),
                                      int(driving_time), int(charging_time))
    return time


def strfdelta(tdelta):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    if tdelta.days:
        if d["hours"] == 1:
            return "{days} jours {hours} heure {minutes} minutes".format(**d)
        return "{days} jours {hours} heures {minutes} minutes".format(**d)
    else:
        if d["hours"] == 1:
            return "{hours} heure {minutes} minutes".format(**d)
        return "{hours} heures {minutes} minutes".format(**d)


@app.route('/', methods=['GET', 'POST'])
def main():
    test = ChargeTrip("audi q4")
    test.get_jsona()
    total_time = None
    charging_time = None
    origin = ""
    destination = ""
    list_positions = []
    waypoints_markers = []

    if (request.form.get('origin')):
        origin = request.form.get('origin')

    if (request.form.get('destination')):
        destination = request.form.get('destination')

    if origin and destination:
        origin_place = MapboxPlace(origin)
        destination_place = MapboxPlace(destination)
        direction = MapboxDirection(origin_place.get_position(), destination_place.get_position())

        origin = origin_place.get_place_name()
        destination = destination_place.get_place_name()

        for positions_no_battery in direction.get_position_charge_needed(60):
            position_charger = ChargingStation(positions_no_battery).get_position()
            if position_charger:
                list_positions.append(position_charger)

        new_direction = MapboxDirection(origin_place.get_position(), destination_place.get_position(), list_positions)

        charging_time_car = 30 * 60
        charging_time = strfdelta(datetime.timedelta(seconds=charging_time_car * len(list_positions)))
        total_time = strfdelta(datetime.timedelta(
            seconds=retrieve_total_travel_time(len(list_positions), new_direction.get_duration(), charging_time_car)))
        waypoints_markers = build_json_waypoint_markers(list_positions)

        if direction.get_distance() > 500:
            print(direction.get_distance())

    return render_template('index.html', travel_time=total_time, charging_time=charging_time, ACCESS_KEY=Config.MAPBOX_ACCESS_KEY, origin=origin,
                           destination=destination, waypoints=list_positions, waypoints_markers=waypoints_markers)


if __name__ == '__main__':
    app.run(debug=True)
