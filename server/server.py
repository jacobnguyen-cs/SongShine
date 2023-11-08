from flask import Flask, jsonify        # pip install 
from flask_cors import CORS             # pip install flask_cors
from geopy.geocoders import Nominatim   # pip install geopy
from dotenv import load_dotenv          # pip install python-dotenv
import requests                         # pip install requests
import os
import base64                           # for encoding
import json

app = Flask(__name__)
CORS(app)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
  auth_string = client_id + ":" + client_secret
  auth_bytes = auth_string.encode("utf-8")
  auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

  url = "https://accounts.spotify.com/api/token"
  headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded"
  }
  data = {"grant_type": "client_credentials"}
  result = requests.post(url, headers=headers, data=data)
  json_result = json.loads(result.content)
  token = json_result["access_token"]
  return token

def get_auth_header(token):
  return {"Authorization" : "Bearer " + token}

### WORKS ###
# def search_for_aritst(token, artist_name):
#   url = "https://api.spotify.com/v1/search"
#   headers = get_auth_header(token)
#   query = f"?q={artist_name}&type=artist&limit=1"

#   query_url = url + query
#   result = requests.get(query_url, headers=headers)
#   json_result = json.loads(result.content)
#   return json_result

### NOT WORKING ###
# def get_top_artists(token):
#   url = "https://api.spotify.com/v1/me/top/artists"
#   headers = get_auth_header(token)
#   result_byte = requests.get(url, headers=headers)
#   result_string = str(result_byte)
#   return result_string

token = get_token()
# print(search_for_aritst(token, "Hozier"))
# print(get_top_artists(token))

# ### Get coordinates ###
# loc = Nominatim(user_agent="GetLoc")
# getLoc = loc.geocode("College Station")
# coordinates = "%.2f, %.2f" % (getLoc.latitude, getLoc.longitude)

# ### GET Request to WeatherAPI with  coordinates ###
# url = "https://weatherapi-com.p.rapidapi.com/current.json"
# querystring = {"q": coordinates} # College Station, TX Latitude and Longitude Coordinates
# headers = {
#   "X-RapidAPI-Key": "",
#   "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
# }
# response = requests.get(url, headers=headers, params=querystring)

# # print(response.json())
# print(response.json()["current"]["condition"])

if __name__ == "__main__":
  app.run(debug=True, port=8080)

### SAMPLE CODE For HTTP Requests ###
# @app.route("/", methods=['GET'])
# def home():
#   url = "https://weatherapi-com.p.rapidapi.com/current.json"
#   loc = Nominatim(user_agent="GetLoc")
#   getLoc = loc.geocode("College Station")
#   coordinates = "%.2f, %.2f" % (getLoc.latitude, getLoc.longitude)
#   querystring = {"q": coordinates} # College Station, TX Latitude and Longitude Coordinates
#   headers = {
#     "X-RapidAPI-Key": "",
#     "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
#   }
#   response = requests.get(url, headers=headers, params=querystring)
#   return response.json()