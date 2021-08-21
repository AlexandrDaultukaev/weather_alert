import requests
import json
import smtplib

params = {
    "exclude": "current,minutely,daily,alerts"
}

email: str
password: str
UTC: int
full_params = {}
forecast: str
date: str


def settings():
    global params, email, password, UTC, full_params
    try:
        with open("credentials.json", "r") as file:
            data = json.load(file)
            params["lon"] = data["lon"]
            params["lat"] = data["lat"]
            params["appid"] = data["appid"]
            params["lang"] = data["lang"]
            email = data["email"]
            password = data["password"]
            UTC = data["UTC"]
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        params["lon"] = float(input("Enter longitude of your city: "))
        params["lat"] = float(input("Enter latitude of your city: "))
        params["appid"] = input("Enter APPID(from openweathermap.org): ")
        params["lang"] = input("Enter language(ru/en): ").title()
        email = input("Enter your EMAIL: ")
        password = input("Enter your password: ")
        UTC = input("Enter your Current Offset time from UTC/GMT: ")
        full_params = params
        full_params.update({"email": email, "password": password, "UTC": UTC})
        with open("credentials.json", "w") as data:
            json.dump(full_params, data)


def current_time_zone(time: str) -> str:
    current_time = int(time.split(":")[0]) + int(UTC)
    if current_time >= 24:
        current_time -= 24
    return str(current_time) + ":00:00"


def check_weather():
    global forecast, date
    key = 0
    hourly_forecast = []
    for hour in weather_data["hourly"][:12]:
        if int(hour["weather"][0]["id"]) < 800 and key == 0:
            key = 1
            if params["lang"] in ["RU", "Ru", "ru", "RUS", "Rus", "rus"]:
                forecast = "Советуем взять зонт.\n"
            else:
                forecast = "Better to take an umbrella.\n"
        converter = requests.get(f"https://showcase.api.linx.twenty57.net/UnixTime/fromunix?timestamp={hour['dt']}")
        converter.raise_for_status()
        date = converter.json().split(' ')[0]
        hourly_forecast.append(f"{current_time_zone(converter.json().split(' ')[1])}: {hour['weather'][0]['description']}")
    if key == 0:
        if params["lang"] in ["RU", "Ru", "ru", "RUS", "Rus", "rus"]:
            forecast = "Вероятнее всего дождя не будет.\n"
        else:
            forecast = "Most likely it won't rain.\n"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email, to_addrs=email,
                            msg=("Subject: " + forecast + "\n\n" + date + ":\n" + '\n'.join(hourly_forecast)).encode("utf-8"))


settings()
response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
response.raise_for_status()
weather_data = response.json()
check_weather()
