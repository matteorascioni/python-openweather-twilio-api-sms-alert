# Before to run this program this program run this commands:
# python3 -m venv venv
# pip3 install requests
# pip3 install twilio
import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Twilio Account: (https://www.twilio.com/)
ACCOUNT_SID = "Twilio: ACCOUNT SID"
AUTH_TOKEN = os.environ.get("Twilio:AUTH_TOKEN")

# OpenWeather Endpoint and APY_KEY (https://openweathermap.org/api)
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
APY_KEY = os.environ.get("OWM_API_KEY")

weather_params = {
    # To get your lat and lon parameters follow this link: https://www.latlong.net/
    "lat": "YOUR LATITUDE",
    "lon": "YOUR LONGITUDE",
    "appid": APY_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    #Check if the weather will be rainy or snowy, etc.
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    # Twilio's proxy configuration.
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=proxy_client)
    # Twilio's body message.
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
    print(message.status)