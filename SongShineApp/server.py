from flask import Flask, jsonify, redirect, request, session, render_template, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
from collections import Counter
from openai import OpenAI

import requests
import os
import urllib.parse
import random
import string

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
CORS(app)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

top_items = []
recommendations = {}

@app.route('/')
def index():
  if 'user_id' in session:
    user_id = session['user_id']
    return render_template('index.html', username=user_id)
  else:
    return render_template('index.html', username='Guest')

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

    # Fetch user profile
    headers = {
      'Authorization' : f"Bearer {token_info['access_token']}"
    }
    user_response = requests.get(API_BASE_URL + '/me', headers=headers)
    user_data = user_response.json()

    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
    session['user_id'] = user_data['id']

    return redirect(url_for('index'))
  
@app.route('/top_items')
def get_top_items():
  if 'access_token' not in session:
    return redirect('/login')
  
  if datetime.now().timestamp() > session['expires_at']:
    return redirect('/refresh-token')
  
  global top_items
  
  headers = {
    'Authorization' : f"Bearer {session['access_token']}"
  }

  response = requests.get(API_BASE_URL + '/me/top/artists?time_range=medium_term&limit=50', headers=headers)
  response = response.json()

  genres = []

  for item in response["items"]:
    top_items.append({
      "id": item["id"],
      "name": item["name"],
      "genres": item["genres"],
      "images": item["images"]
    })

  genres.extend(item["genres"])
  
  top_genres = [genre for genre, _ in Counter(genres).most_common(5)]

  return jsonify({ "top_items": top_items, "top_genres": top_genres })

def get_recommendations(pref_genre):
  global top_items
  global recommendations

  url = API_BASE_URL + '/recommendations?limit=50'
  seed_artists = '&seed_artists='
  seed_genres = '&seed_genres='
  headers = {
    'Authorization' : f"Bearer {session['access_token']}"
  }

  genre_map = {}
  for item in top_items:
    for genre in item['genres']:
      genre_map[genre] = 1 + genre_map.get(genre, 0)

  pref_artists = []
  for item in top_items:
    if pref_genre not in item['genres']:
      continue
    pref_artists.append(item['id'])

  seed_genres += pref_genre

  for i in range(len(pref_artists)):
    if i == 3:
      break
    
    seed_artists += pref_artists[i]
    if i != len(pref_artists) - 1:
      seed_artists += ','

  url = url + seed_artists + seed_genres
  response = requests.get(url, headers=headers)
  response = response.json()

  # for tracks in response['tracks']:
  #   recommendations[(tracks['album']['name'] + ' by ' + tracks['album']['artists'][0]['name'])] = tracks['album']['artists'][0]['id']

  recs = ""

  for i, tracks in enumerate(response['tracks']):
    recs += str(i + 1) + '. '+ tracks['album']['name'] + ' by ' + tracks['album']['artists'][0]['name'] + '\n'

  return recs

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

    return redirect('/top_items')


# OpenAI API section
@app.route('/get_recs', methods=(["POST"]))
def get_song_recommendations():
  if 'access_token' not in session:
    return redirect('/login')
  
  if datetime.now().timestamp() > session['expires_at']:
    return redirect('/refresh-token')
    
  print('in get_song_recommendations')

  data = request.get_json()
  genre = data.get('genre')
  condition = data.get('condition')
  temp = data.get('temp')

  spotify_recs = get_recommendations(genre)
  recommendations = generate_song_recommendations(spotify_recs, condition, temp)

  return(jsonify({'recommendations': recommendations}))

def generate_song_recommendations(spotify_recs, weather_condition, temperature):
  print("IN GENERATE_SONG_RECOMMENDATIONS")
  
  client = OpenAI()
  client.api_key = os.getenv("OPENAI_API_KEY")
  # openai.api_key = os.getenv("OPENAI_API_KEY")

  # Make a request to the ChatGPT API
  msgs = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"I like listening to these albums whic are listed in no particular order {spotify_recs}. It is also currently {temperature} degrees fahrenheit and {weather_condition} where I am at. Can you pick 5 songs from these albums based on the current weather? (Format the list exactly like this: \"1. <song name 1> by <song artist 1>\n2. <song name 2> by <song artist 2>\" and so on)"}
  ]

  bot = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=msgs,
  )

  reply = bot.choices[0].message
  print("GPT REPLY:\n", reply, "\n")
  return reply.content

if __name__ == "__main__":
  app.run(debug=True, port=8080)
