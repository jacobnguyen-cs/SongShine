# SongShine
## Video
https://drive.google.com/file/d/12x17uzGxLWbtjEEfTPssE8hv9Rj30-jm/view?usp=drive_link
## How to Run
```
cd SongShineApp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python server.py
```
## About
SongShine is a weather-based music recommender application. Given the current weather (sunny, gloomy, hot, cold, etc.) and a specified genre, our application will recommend 5 songs. \
The application will take into account components of your Spotify account, including top artists from the last month, top tracks from the last month, and contents in your playlists. 

## API
Three APIs were used to build this application. \
The first - a weather API was used to find the precise geolocation for a given user and based on that information, output and store the current temperature, what temperature it feels like, and a general weather condition for this location. \
The second API we used was a Spotify API to track the logged in user's account information including their account name, top artists from the last 50 days, and top genres based on their top artists. \
The final API that we used was a ChatGPT API. This allowed us to take the learned information of the weather in the user's current location, pair that with a specified genre, and ultimately recommend a list of songs that the user will hopefully enjoy.

## Credits
weatherapi.com - weather API \
Spotify - Spotify API \
OpenAI - ChatGPT API
