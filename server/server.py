from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def home():
  url = "https://weatherapi-com.p.rapidapi.com/current.json"

  querystring = {"q":"30.6, -96.3"} # College Station, TX Latitude and Longitude Coordinates

  headers = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)
  
  return response.json()

if __name__ == "__main__":
  app.run(debug=True, port=8080)
