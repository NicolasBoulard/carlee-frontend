from os import environ
class Config(object):
    MAPBOX_ACCESS_KEY = environ.get('MAPBOX_ACCESS_KEY')
    MAPBOX_PUBLIC_ACCESS_KEY = environ.get('MAPBOX_PUBLIC_ACCESS_KEY')
    CARLEE_SOAP = environ.get('CARLEE_SOAP')
    CHARGETRIP_CLIENT_ID = environ.get('CHARGETRIP_CLIENT_ID')
    CHARGETRIP_APP_ID = environ.get('CHARGETRIP_APP_ID')
    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
