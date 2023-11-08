from flask import Flask, jsonify, redirect, request, session        # pip install flask
from flask_cors import CORS                                         # pip install flask_cors
from geopy.geocoders import Nominatim                               # pip install geopy
from dotenv import load_dotenv                                      # pip install python-dotenv
from datetime import datetime
import requests                                                     # pip install requests
import os
import urllib.parse

app = Flask(__name__)
app.secret_key = "s4zqSdQoqb2tR8RB"
CORS(app)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

@app.route('/')
def index():
  return "Welcome to SongShine <a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
  scope = 'user-read-private user-top-read'
  params = {
    'client_id': client_id,
    'response_type': 'code',
    'scope': scope,
    'redirect_uri': REDIRECT_URI,
    'show_dialog': True
  }

  auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

  return redirect(auth_url)

@app.route('/callback')
def callback():
  if 'error' in request.args:
    return jsonify({"error": request.args["error"]})
  
  if 'code' in request.args:
    req_body = {
      'code': request.args['code'],
      'grant_type': 'authorization_code',
      'redirect_uri' : REDIRECT_URI,
      'client_id': client_id,
      'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=req_body)
    token_info = response.json()

    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    return redirect('/artists')
  
@app.route('/artists')
def get_artists():
  if 'access_token' not in session:
    return redirect('/login')
  
  if datetime.now().timestamp() > session['expires_at']:
    return redirect('/refresh-token')
  
  headers = {
    'Authorization' : f"Bearer {session['access_token']}"
  }

  response = requests.get(API_BASE_URL + '/me/top/artists', headers=headers)
  artists = response.json()

  return artists

@app.route('/refresh-token')
def refresh_token():
  if 'refresh_token' not in session:
    return redirect('/login')
  
  if datetime.now().timestamp() > session['expires_at']:
    req_body = {
      'grant_type': 'refresh_token',
      'refresh_token': session['refresh_token'],
      'client_id': client_id,
      'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect('/artists')

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