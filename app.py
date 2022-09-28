from typing import List

from flask import Flask, render_template, request
from zeep import Client

from services import MapboxDirection, MapboxPlace, ChargingStation
from settings import Config
import requests
import datetime
from geojson import Point

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def retrieve_total_travel_time(driving_time: int, charging_time: int):
    client = Client('http://localhost:8000/?wsdl')
    time = client.service.travel_time(
        int(driving_time), int(charging_time))
    return time

def strfdelta(tdelta):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    if tdelta.days:
        return "{days} jours {hours} heures {minutes} minutes".format(**d)
    else:
        return "{hours} heures {minutes} minutes".format(**d)

@app.route('/', methods=['GET', 'POST'])
def main():
    total_time = None
    origin = ""
    destination = ""
    list_positions = []

    if (request.form.get('origin')):
        origin = request.form.get('origin')

    if (request.form.get('destination')):
        destination = request.form.get('destination')

    if origin and destination:
        origin_place = MapboxPlace(origin)
        destination_place = MapboxPlace(destination)
        direction = MapboxDirection(origin_place.get_position(), destination_place.get_position())

        total_time = strfdelta(datetime.timedelta(seconds=retrieve_total_travel_time(direction.get_duration(), 30 * 60)))
        origin = origin_place.get_place_name()
        destination = destination_place.get_place_name()

        for positions_no_battery in direction.get_position_charge_needed(60):
            position_charger = ChargingStation(positions_no_battery).get_position()
            if position_charger:
                list_positions.append(Point(position_charger)['coordinates'])
        print(list_positions)

        if direction.get_distance() > 500:
            print(direction.get_distance())

    return render_template('index.html', travel_time=total_time, ACCESS_KEY=Config.MAPBOX_ACCESS_KEY, origin=origin,
                           destination=destination, waypoints=list_positions)


if __name__ == '__main__':
    app.run(debug=True)
