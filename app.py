from typing import List

from flask import Flask, render_template, request
from zeep import Client

from services import MapboxDirection, MapboxPlace, ChargingStation, ChargeTrip, ChargeTripCar
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
    client = Client(f"{Config.CARLEE_SOAP}/?wsdl")
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

@app.route('/car', methods=['POST', 'GET'])
def car():
    if request.data:
        car_list = ChargeTrip(request.data.decode("utf-8"))
        return car_list.get_car_list()
    return 'No data provided', 400


@app.route('/', methods=['GET', 'POST'])
def main():
    car_id = ""
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

    if (request.form.get('car-selected')):
        car_id = request.form.get('car-selected')
        print(car_id)

    if origin and destination and car_id:
        origin_place = MapboxPlace(origin)
        destination_place = MapboxPlace(destination)
        direction = MapboxDirection(origin_place.get_position(), destination_place.get_position())

        origin = origin_place.get_place_name()
        destination = destination_place.get_place_name()

        car = ChargeTripCar(car_id)
        car_autonomy = car.get_mean_km()

        for positions_no_battery in direction.get_position_charge_needed(car_autonomy):
            position_charger = ChargingStation(positions_no_battery).get_position()
            if position_charger:
                list_positions.append(position_charger)

        new_direction = MapboxDirection(origin_place.get_position(), destination_place.get_position(), list_positions)

        charging_time_car = 30 * 60
        charging_time = strfdelta(datetime.timedelta(seconds=charging_time_car * len(list_positions)))
        total_time = strfdelta(datetime.timedelta(
            seconds=retrieve_total_travel_time(len(list_positions), new_direction.get_duration(), charging_time_car)))
        waypoints_markers = build_json_waypoint_markers(list_positions)

    return render_template('index.html', travel_time=total_time, charging_time=charging_time, ACCESS_KEY=Config.MAPBOX_ACCESS_KEY, origin=origin,
                           destination=destination, waypoints=list_positions, waypoints_markers=waypoints_markers, APP_URL=Config.APP_URL)


if __name__ == '__main__':
    app.run(debug=True)
