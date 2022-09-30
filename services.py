from typing import List
from settings import Config
import requests

MAPBOX_HEADERS = {'Content-type': 'application/x-www-form-urlencoded',
                  'Host': 'api.mapbox.com'}
OPENDATA_HEADERS = {'Content-type': 'application/x-www-form-urlencoded',
                    'Host': 'odre.opendatasoft.com'}


class MapboxDirection:
    """
    Mapbox API interaction for retreiving direction
    """

    def __init__(self, origin_pos, destination_pos, waypoints=None):
        waypoints_str = ""
        if waypoints:
            for wp in waypoints:
                waypoints_str += f";{wp[0]},{wp[1]}"

        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin_pos[0]},{origin_pos[1]}{waypoints_str};{destination_pos[0]},{destination_pos[1]}?access_token={Config.MAPBOX_PUBLIC_ACCESS_KEY}&steps=true"
        request = requests.get(url, headers=MAPBOX_HEADERS)

        if request.status_code == 200:
            self.direction_service = request.json()
        else:
            raise Exception("Error while calling mapbox api (status code != 200)")

    def get_duration(self):
        return self.direction_service.get('routes')[0].get('duration')

    def get_distance(self):
        return round(self.direction_service.get('routes')[0].get('distance')/1000)

    def get_position_charge_needed(self, distance):
        current_distance = 0
        positions_battery_limit = []
        for step in self.direction_service.get('routes')[0].get('legs')[0].get('steps'):
            current_distance += float(step.get('distance')/1000)
            if current_distance > distance:
                positions_battery_limit.append(step)
                current_distance = 0
        positions_lon_lan = []
        for positions in positions_battery_limit:
            positions_lon_lan.append(positions.get('intersections')[-1].get('location'))
        return positions_lon_lan




class MapboxPlace:
    """
    Mapbox API interaction for retreiving place
    """

    def __init__(self, place_name: str):
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place_name}.json?access_token={Config.MAPBOX_PUBLIC_ACCESS_KEY}"
        request = requests.get(url, headers=MAPBOX_HEADERS)

        if request.status_code == 200:
            self.place_service = request.json()
        else:
            raise Exception("Error while calling mapbox api (status code != 200)")

    def get_position(self) -> List[float]:
        return self.place_service.get('features')[0].get('center')

    def get_place_name(self):
        return self.place_service.get('features')[0].get('place_name')


class ChargingStation:
    """
    Opendatasoft API interaction for retreiving charging point
    """

    def __init__(self, waypoint_pos):
        url = f"https://odre.opendatasoft.com/api/records/1.0/search/?dataset=bornes-irve&q=&rows=1&sort=-dist&facet=region&facet=departement&geofilter.distance={waypoint_pos[0]},{waypoint_pos[1]},+100000"
        request = requests.get(url, headers=OPENDATA_HEADERS)

        if request.status_code == 200:
            self.charging_station_service = request.json()
        else:
            raise Exception("Error while calling opendatasoft api (status code != 200)")

    def get_position(self):
        if len(self.charging_station_service['records']) > 0:
            return self.charging_station_service['records'][0]['fields']['geo_point_borne']
        else:
            return None
