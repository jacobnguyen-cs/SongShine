from flask import Flask, jsonify        # pip install 
from flask_cors import CORS             # pip install flask_cors
from geopy.geocoders import Nominatim   # pip install geopy
import requests                         # pip install requests

app = Flask(__name__)
CORS(app)

### SAMPLE CODE For HTTP Requests ###
# @app.route("/", methods=['GET'])
# def home():
#   url = "https://weatherapi-com.p.rapidapi.com/current.json"
#   loc = Nominatim(user_agent="GetLoc")
#   getLoc = loc.geocode("College Station")
#   coordinates = "%.2f, %.2f" % (getLoc.latitude, getLoc.longitude)
#   querystring = {"q": coordinates} # College Station, TX Latitude and Longitude Coordinates
#   headers = {
#     "X-RapidAPI-Key": "cdc0c19252msh6449b7b29d1bb94p1dcf61jsn236a7bab7b74",
#     "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
#   }
#   response = requests.get(url, headers=headers, params=querystring)
#   return response.json()

### Get coordinates ###
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("College Station")
coordinates = "%.2f, %.2f" % (getLoc.latitude, getLoc.longitude)

### GET Request to WeatherAPI with  coordinates ###
url = "https://weatherapi-com.p.rapidapi.com/current.json"
querystring = {"q": coordinates} # College Station, TX Latitude and Longitude Coordinates
headers = {
  "X-RapidAPI-Key": "cdc0c19252msh6449b7b29d1bb94p1dcf61jsn236a7bab7b74",
  "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring)

# print(response.json())
print(response.json()["current"]["condition"])


if __name__ == "__main__":
  app.run(debug=True, port=8080)
