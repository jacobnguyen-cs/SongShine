let weatherData;
let chosenGenre;

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded fired")

    function openPopup(title, content) {
        console.log("openPopup fired")

        const overlay = document.createElement("div");
        overlay.classList.add("overlay");

        const popup = document.createElement("div");
        popup.classList.add("popup");

        const popupHeader = document.createElement("div");
        popupHeader.classList.add("popup-header");

        const titleElement = document.createElement("h2");
        titleElement.innerHTML = title;

        const closeButton = document.createElement("button");
        closeButton.classList.add("close-button");
        closeButton.innerHTML = "X";
        closeButton.addEventListener("click", function () {
            overlay.remove();
        });

        popupHeader.appendChild(titleElement);
        popupHeader.appendChild(closeButton);

        const popupContent = document.createElement("div");
        popupContent.classList.add("popup-content");
        popupContent.innerHTML = content;

        popup.appendChild(popupHeader);
        popup.appendChild(popupContent);

        overlay.appendChild(popup);
        document.body.appendChild(overlay);
    }

    const loader = document.createElement("div");
    loader.classList.add("loader");

    function showLoader() {
        const locateMeButton = document.querySelector(".hero--btn");
        locateMeButton.insertAdjacentElement("afterend", loader);
    }

    function hideLoader() {
        if (document.body.contains(loader)) {
            loader.remove();
        }
    }

    function getLocation() {
        showLoader();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                console.log("Latitude: " + latitude);
                console.log("Longitude: " + longitude);

                const weatherApiKey = "c00501fae64942e18c6183807231711";
                const weatherApiUrl = `http://api.weatherapi.com/v1/current.json?key=${weatherApiKey}&q=${latitude},${longitude}&aqi=no`;

                fetch(weatherApiUrl)
                    .then(response => response.json())
                    .then(data => {
                        hideLoader();
                        weatherData = data;  // Storing weather data globally
                        
                        const weatherCard = document.querySelector(".weather-card");

                        const locationText = document.querySelector(".default--vals.location");
                        const temperatureText = document.querySelector(".default--vals.temperature");
                        const feelsLikeText = document.querySelector(".default--vals.feels-like");
                        const conditionText = document.querySelector(".default--vals.weather-condition");
                    
                        locationText.textContent = `${data.location.name}, ${data.location.region}, ${data.location.country}`;
                        temperatureText.textContent = `${data.current.temp_f} °F`;
                        feelsLikeText.textContent = `${data.current.feelslike_f} °F`;
                        conditionText.textContent = data.current.condition.text;
                    
                        
                        const weatherIcon = document.createElement("img");
                        weatherIcon.src = `http:${data.current.condition.icon}`;
                        weatherIcon.alt = data.current.condition.text;
                    
                        
                        const weatherImg = document.querySelector(".weather--img");
                        weatherImg.src = weatherIcon.src;
                        weatherImg.alt = weatherIcon.alt;
                    
                        const weatherWidget = document.querySelector(".weather--widget");
                        weatherWidget.innerHTML = "";
                        weatherWidget.appendChild(weatherCard);
                    })
                    .catch(error => {
                        hideLoader();
                        console.error("Error fetching weather data:", error);
                    });
            }, function (error) {
                hideLoader();
                console.error("Error getting location:", error.message);
            });
        } else {
            hideLoader();
            console.error("Geolocation is not supported by this browser.");
        }
    }

    const aboutLink = document.querySelector(".navbar--link.about");
    aboutLink.addEventListener("click", function () {
        const aboutContent = "SongShine is a weather-based music recommender application. Given the current weather (sunny, gloomy, hot, cold, etc.) and a specified genre, our application will recommend 5 songs. <br><br> The application will take into account components of your Spotify account, including top artists from the last month, top tracks from the last month, and contents in your playlists.";
        openPopup("About", aboutContent);
    });

    const apisLink = document.querySelector(".navbar--link.apis");
    apisLink.addEventListener("click", function () {
        const apisContent = "Three APIs were used to build this application. <br><br> The first - a weather API was used to find the precise geolocation for a given user and based on that information, output and store the current temperature, what temperature it feels like, and a general weather condition for this location.  <br><br> The second API we used was a Spotify API to track the logged in user's account information including their account name, top artists from the last 50 days, and top genres based on their top artists. <br><br> The final API that we used was a ChatGPT API. This allowed us to take the learned information of the weather in the user's current location, pair that with a specified genre, and ultimately recommend a list of songs that the user will hopefully enjoy.";
        openPopup("APIs", apisContent);
    });

    const creditsLink = document.querySelector(".navbar--link.credits");
    creditsLink.addEventListener("click", function () {
        const creditsContent = "weatherapi.com - weather API<br><br>Spotify - Spotify API<br><br> OpenAI - ChatGPT API";
        openPopup("Credits", creditsContent);
    });

    const locateMeButton = document.querySelector(".hero--btn");
    locateMeButton.addEventListener("click", function () {
        getLocation();
    });
});

document.getElementById('loginButton').addEventListener('click', () => {
    window.location.href = 'http://localhost:8080/login';
});

document.getElementById('topItemsButton').addEventListener('click', () => {
    fetch('http://localhost:8080/top_items')
        .then(response => response.json())
        .then(data => {
            console.log('Top Artists: ', data.top_items);
            console.log('Top Genres:', data.top_genres);
            displayTopArtists(data.top_items);
            displayTopGenres(data.top_genres, weatherData);
        })
        .catch(error => console.error('Error fetching top items:', error));
});

const loader2 = document.createElement("div");
loader2.classList.add("loader");

function showLoader2() {
    const locateMeButton = document.querySelector(".genre-btns");
    locateMeButton.insertAdjacentElement("afterend", loader2);
}

function hideLoader2() {
    if (document.body.contains(loader2)) {
        loader2.remove();
    }
}

function displayTopGenres(topGenres, weather) {
    const genreButtonsContainer = document.querySelector('.genre-btns');
    const songRecsContainer = document.querySelector('.song-recommendations');
    const songRecHeader = document.querySelector('.songRecHeader');
    const genreButtons = document.querySelectorAll('.gere-btns');
    const genreIntroText = document.getElementById('genreIntroText');
    const songList = document.querySelector('.song-list');
    
    topGenres.forEach((genre, index) => {
        const button = genreButtons[index];
        if (button) {
            button.style.display = 'block';
            button.textContent = genre;
        }
        
        button.addEventListener('click', () => {
            showLoader2();
            chosenGenre = genre;
            let condition = weatherData.current.condition.text;
            let temp = weatherData.current.temp_f;

            // Retrieving recommendations from chatgpt
            const _data = {
                genre: chosenGenre,
                condition: condition,
                temp: temp
            };
            
            fetch('/get_recs', {
                method: 'POST',
                body: JSON.stringify(_data),
                headers:{
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error. Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                hideLoader2();
                const songRecommendationString = data.recommendations;
                const parsedSongs = parseSongRecommendations(songRecommendationString);
                // const songList = document.querySelector('.song-list');
                console.log("Parsed Songs:", parsedSongs);
                songList.innerHTML = '';
                parsedSongs.forEach((song, index) => {
                    fetch(`/get_uri?song=${song}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log('Track data: ', data.track_data, 'Artist Data: ', data.artist_data);
                        })
                        .catch(error => console.error('Error while fetching song data: ', error));
                    const songItem = document.createElement('li');
                    songItem.classList.add('artist-item');
                    songItem.textContent = song;
                    songItem.innerHTML = `<span class="artist-number">${index + 1}.</span> <span class="artist-name">${song}</span>`
                    songList.appendChild(songItem);
                });
                songRecsContainer.style.visibility = 'visible';
                songRecsContainer.style.display = 'flex';
                songRecsContainer.style.flexDirection = 'column';
                songRecHeader.style.margin = '20px';
            });
        });
    });

    genreIntroText.textContent = "Here are your favorite genres from the last 6 months. Select which genre of music you want recommendations for.";
    genreButtonsContainer.style.visibility = 'visible';
    genreButtonsContainer.style.display = 'flex';
}

function displayTopArtists(topArtists) {
    const artistList = document.getElementById('artistList');
    if (!artistList) {
        console.error('Element with id "artistList" not found');
        return;
    }
    
    artistList.innerHTML = '';

    topArtists.slice(0, 10).forEach((artist, index) => {
        const artistCard = document.createElement('div');
        artistCard.classList.add('artist-card');

        const artistImage = document.createElement('img');
        artistImage.src = artist.images[1].url;
        artistImage.classList.add('artist-image');

        const artistInfo = document.createElement('div');
        artistInfo.classList.add('artist-info');

        artistInfo.innerHTML = `<span class="artist-number">${index + 1}.</span> <span class="artist-name">${artist.name}</span> (${artist.genres.join(', ')})`;

        artistCard.appendChild(artistImage);
        artistCard.appendChild(artistInfo);

        artistList.appendChild(artistCard);
    });
}

function parseSongRecommendations(chatOutput) {
    // Use regular expression to extract the song recommendations part
    const regex = /1\. "(.+?)" by (.+?)\n2\. "(.+?)" by (.+?)\n3\. "(.+?)" by (.+?)\n4\. "(.+?)" by (.+?)\n5\. "(.+?)" by (.+?)\n/;
    const match = chatOutput.match(regex);
    if (match) {
        // Extract individual song recommendations and artists
        const songs = [];
        for (let i = 1; i <= 10; i += 2) {
            const song = `${match[i]} by ${match[i + 1]}`;
            songs.push(song.trim());
        }
        return songs;
    } else {
        return null;
    }
}