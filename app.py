from typing import List

from flask import Flask, render_template, request
from zeep import Client
from settings import Config
import requests
import datetime

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def retrieve_total_travel_time(driving_time:int,charging_time:int):
    client = Client('http://localhost:8000/?wsdl')
    print(int(driving_time))
    print(int(charging_time))
    time = client.service.travel_time(
        int(driving_time), int(charging_time))
    return time


def get_direction_duration(origin_lon_lat,dest_lon_lat):
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Host': 'api.mapbox.com'}
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin_lon_lat[0]},{origin_lon_lat[1]};{dest_lon_lat[0]},{dest_lon_lat[1]}?access_token={Config.MAPBOX_PUBLIC_ACCESS_KEY}"
    result = requests.get(url, headers=headers)
    return result.json().get('routes')[0].get('duration')


def get_lon_lat_position(search: str) -> List[float]:
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'Host': 'api.mapbox.com'}
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{search}.json?access_token={Config.MAPBOX_PUBLIC_ACCESS_KEY}"
    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        return result.json().get('features')[0].get('center')


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
        place = origin
        origin_lon_lat = get_lon_lat_position(origin)
        dest_lon_lat = get_lon_lat_position(destination)
        direction_duration = get_direction_duration(origin_lon_lat, dest_lon_lat)
        print(direction_duration)

        total_time = datetime.timedelta(seconds=retrieve_total_travel_time(direction_duration, 30*60))


    return render_template('index.html', travel_time=total_time, ACCESS_KEY=Config.MAPBOX_ACCESS_KEY, origin=origin,
                           destination=destination)


if __name__ == '__main__':
    app.run(debug=True)
