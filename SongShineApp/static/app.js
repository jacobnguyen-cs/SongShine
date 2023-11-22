
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
                        // const weatherCard = document.createElement("div");
                        // weatherCard.classList.add("weather-card");

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
        const aboutContent = "SongShine is a weather-based music recommender application. Given the current weather (sunny, gloomy, hot, cold, etc.) and a specified genre, our application will recommend 5 songs. The application will take into account components of your Spotify account, including top artists from the last month, top tracks from the last month, and contents in your playlists.";
        openPopup("About", aboutContent);
    });

    const apisLink = document.querySelector(".navbar--link.apis");
    apisLink.addEventListener("click", function () {
        const apisContent = "Three APIs were used to build this application. The first - a weather API was used to find the precise geolocation for a given user and based on that information, output and store the current temperature, what temperature it feels like, and a general weather condition for this location. The second API we used was a Spotify API to track the logged in user's account information including their account name, top artists and tracks from the last month, and contents of their playlists. The final API that we used was a ChatGPT API. This allowed us to take the learned information of the weather in the user's current location, pair that with a specified genre, and ultimately recommend a list of songs that the user will hopefully enjoy.";
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

document.getElementById('genre-btn-0').addEventListener('click', () => {
    console.log('button0');
});

document.getElementById('genre-btn-1').addEventListener('click', () => {
    console.log('button1');
});

document.getElementById('genre-btn-2').addEventListener('click', () => {
    console.log('button2');
});

document.getElementById('genre-btn-3').addEventListener('click', () => {
    console.log('button3');
});

document.getElementById('genre-btn-4').addEventListener('click', () => {
    console.log('button4');
});