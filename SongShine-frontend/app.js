
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
        const aboutContent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget justo id augue ullamcorper consequat.<br><br>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.";
        openPopup("About", aboutContent);
    });

    const apisLink = document.querySelector(".navbar--link.apis");
    apisLink.addEventListener("click", function () {
        const apisContent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget justo id augue ullamcorper consequat.<br><br>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.";
        openPopup("APIs", apisContent);
    });

    const creditsLink = document.querySelector(".navbar--link.credits");
    creditsLink.addEventListener("click", function () {
        const creditsContent = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget justo id augue ullamcorper consequat.<br><br>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.";
        openPopup("Credits", creditsContent);
    });

    const locateMeButton = document.querySelector(".hero--btn");
    locateMeButton.addEventListener("click", function () {
        getLocation();
    });
});