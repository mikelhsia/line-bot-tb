import requests

APP_SECRET = '57ef6585e30d509801a5ce0a09496021'
LOCATION = 'Taipei'
OPEN_WEATHER_API_URL = f'http://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&mode=json&appid={APP_SECRET}'

def get_weather():
    try:
        r = requests.get(OPEN_WEATHER_API_URL)
    except BaseException as e:
        abort(400)

    if r.status_code != 200:
        return f"Request status code: {r.status_code}"

    # TODO: Process timestamp. Right now is UTC time
    return f"{r.json()['list'][0]['dt_txt']} is {r.json()['list'][0]['weather'][0]['main']} with {r.json()['list'][0]['weather'][0]['description']}"