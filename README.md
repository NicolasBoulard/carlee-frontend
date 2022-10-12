# Carlee project 🚗
This is a project for course ETRS013 in master 2 at USMB.
The goal of this project is to create a web based app that will communicate with differents api.
There is a SOAP service, REST public api call and a flask app that will communicate with all apps.

## How to use this app ?
**You need to setup carlee backend before [see here](https://github.com/NicolasBoulard/carlee)**
### Without docker

1. Clone this repo `git clone https://github.com/NicolasBoulard/carlee-frontend.git`
2. Create venv `python -m venv .venv`
3. Activate venv `.venv\Script\Activate`
4. Install requirements `pip install -r requirements.txt`
5. Create a .env file with this content `
MAPBOX_ACCESS_KEY=Your_mapbox_access_key
MAPBOX_PUBLIC_ACCESS_KEY=Your_mapbox_public_access_key
CARLEE_SOAP=URL_of_your_carlee_soap_ex_http://localhost:8000
CHARGETRIP_CLIENT_ID=Your_chargetrip_client_id
CHARGETRIP_APP_ID=Your_chargetrip_app_id
APP_URL=Application_url_ex_http://localhost:5000`
6. Launch project `python app.py`

### With docker 🐋
1. Clone this repo `git clone https://github.com/NicolasBoulard/carlee-frontend.git`
2. Build file with using dockerfile `docker build . -t carlee-frontend`
3. Run this image `docker run -e MAPBOX_ACCESS_KEY=Your_mapbox_access_key -e MAPBOX_PUBLIC_ACCESS_KEY=Your_mapbox_public_access_key -e CARLEE_SOAP=URL_of_your_carlee_soap_ex_http://localhost:8000 -e CHARGETRIP_CLIENT_ID=Your_chargetrip_client_id -e CHARGETRIP_APP_ID=Your_chargetrip_app_id -e APP_URL=Application_url_ex_http://localhost:5000 -e PORT=Your_port carlee-frontend`

### Question ?
If you want to contribute to this project/improve code open an issue