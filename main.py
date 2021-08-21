import requests
import json

params = {
    "exclude": "current,minutely,daily,alerts"
}


def settings():
    global params
    try:
        with open("credentials.json", "r") as file:
            data = json.load(file)
            params["lon"] = data["lon"]
            params["lat"] = data["lat"]
            params["appid"] = data["appid"]
            params["lang"] = data["lang"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        params["lon"] = float(input("Enter longitude of your city: "))
        params["lat"] = float(input("Enter latitude of your city: "))
        params["appid"] = input("Enter APPID(from openweathermap.org): ")
        params["lang"] = input("Enter language(ru/en): ").title()
        with open("credentials.json", "w") as data:
            json.dump(params, data)


def check_weather():
    key = 0
    for hour in weather_data["hourly"][:12]:
        if int(hour["weather"][0]["id"]) < 800 and key == 0:
            key = 1
            if params["lang"] in ["RU", "Ru", "ru", "RUS", "Rus", "rus"]:
                print("Советуем взять зонт.\n")
            else:
                print("Better to take an umbrella.\n")
        print(hour["weather"][0]["description"])
    if key == 0:
        if params["lang"] in ["RU", "Ru", "ru", "RUS", "Rus", "rus"]:
            print("Вероятнее всего дождя не будет.\n")
        else:
            print("Most likely it won't rain.\n")

settings()
response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
response.raise_for_status()
weather_data = response.json()
check_weather()

print(weather_data)
