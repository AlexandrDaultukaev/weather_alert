import requests
import json

params = {
    "exclude": "current,minutely,daily,alerts"
}

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






print(params)

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
response.raise_for_status()
weather_data = response.json()
print(weather_data)
