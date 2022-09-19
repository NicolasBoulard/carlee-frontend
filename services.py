from typing import List
from settings import Config
import requests

MAPBOX_HEADERS = {'Content-type': 'application/x-www-form-urlencoded',
                  'Host': 'api.mapbox.com'}


class MapboxDirection:
    """
    Mapbox API interaction for retreiving direction
    """
    def __init__(self, origin_pos, destination_pos):
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin_pos[0]},{origin_pos[1]};{destination_pos[0]},{destination_pos[1]}?access_token={Config.MAPBOX_PUBLIC_ACCESS_KEY}"
        request = requests.get(url, headers=MAPBOX_HEADERS)

        if request.status_code == 200:
            self.direction_service = request.json()
        else:
            raise Exception("Error while calling mapbox api (status code != 200)")


    def get_duration(self):
        return self.direction_service.get('routes')[0].get('duration')


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