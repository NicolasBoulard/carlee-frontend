from typing import List

from flask import Flask, render_template, request
from zeep import Client

from services import MapboxDirection, MapboxPlace
from settings import Config
import requests
import datetime

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


def retrieve_total_travel_time(driving_time: int, charging_time: int):
    client = Client('http://localhost:8000/?wsdl')
    print(int(driving_time))
    print(int(charging_time))
    time = client.service.travel_time(
        int(driving_time), int(charging_time))
    return time


@app.route('/', methods=['GET', 'POST'])
def main():
    total_time = None
    origin = ""
    destination = ""

    if (request.form.get('origin')):
        origin = request.form.get('origin')

    if (request.form.get('destination')):
        destination = request.form.get('destination')

    if origin and destination:
        origin_place = MapboxPlace(origin)
        destination_place = MapboxPlace(destination)
        direction = MapboxDirection(origin_place.get_position(), destination_place.get_position())

        total_time = datetime.timedelta(seconds=retrieve_total_travel_time(direction.get_duration(), 30 * 60))

    return render_template('index.html', travel_time=total_time, ACCESS_KEY=Config.MAPBOX_ACCESS_KEY, origin=origin,
                           destination=destination)


if __name__ == '__main__':
    app.run(debug=True)
