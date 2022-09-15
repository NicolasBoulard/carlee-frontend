from os import environ
class Config(object):
    MAPBOX_ACCESS_KEY = environ.get('MAPBOX_ACCESS_KEY')
    MAPBOX_PUBLIC_ACCESS_KEY = environ.get('MAPBOX_PUBLIC_ACCESS_KEY')