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
  
  headers = {
    'Authorization' : f"Bearer {session['access_token']}"
  }

  response = requests.get(API_BASE_URL + '/me/top/artists?time_range=medium_term&limit=50', headers=headers)
  response = response.json()

  top_items = []
  genres = []

  for item in response["items"]:
    top_items.append({
      "id": item["id"],
      "name": item["name"],
      "genres": item["genres"]
    })

    genres.extend(item["genres"])
  
  top_genres = [genre for genre, _ in Counter(genres).most_common(5)]

  return jsonify({ "top_items": top_items, "top_genres": top_genres })

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
  print('in get_song_recommendations')

  data = request.get_json()
  genre = data.get('genre')
  condition = data.get('condition')
  temp = data.get('temp')

  recommendations = generate_song_recommendations(genre, condition, temp)
  return(jsonify({'recommendations': recommendations}))

def generate_song_recommendations(genre_preferences, weather_condition, temperature):
  print("IN GENERATE_SONG_RECOMMENDATIONS")
  
  client = OpenAI()
  client.api_key = os.getenv("OPENAI_API_KEY")
  # openai.api_key = os.getenv("OPENAI_API_KEY")

  # Make a request to the ChatGPT API
  msgs = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"I like listening to {genre_preferences} music. It is also currently {temperature} degrees fahrenheit and {weather_condition} where I am at. Can you recommend 5 songs based on this genre preference and the current weather? (No need for any introduction, just give me the top 5 list)"}
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
