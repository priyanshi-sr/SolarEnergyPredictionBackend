from flask import Flask, request, jsonify
import requests
import pandas as pd
import joblib
import datetime

API_KEY = 'API_KEY'

app = Flask(__name__)
features = ['Temperature', 'Pressure', 'Humidity', 'WindDirection(Degrees)', 'Speed']
model = joblib.load('model.joblib')


@app.route('/Radiation', methods=['POST'])
def Radiation():
    date = request.json.get('date')
    time = request.json.get('time')  # eg: 12:45
    city = request.json.get('location')

    if not date:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    if not time:
        time = datetime.datetime.now().strftime('%H:%M')

    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    if date < datetime.datetime.now():
        api = 'history'
    elif date < datetime.datetime.now() + datetime.timedelta(days=14):
        api = 'forecast'
    else:
        api = 'future'
    date = date.strftime('%Y-%m-%d')

    hour = time.split(':')[0]
    data = requests.get(
        f'https://api.weatherapi.com/v1/{api}.json?key={API_KEY}&q={city if city else '27.4924,77.6737'}&dt={date}').json()
    if 'error' in data:
        return jsonify(data)
    dataTime = data['forecast']['forecastday'][0]['hour'][int(hour)]
    temperature = dataTime['temp_c']
    humidity = dataTime['humidity']
    speed = dataTime['wind_kph']
    pressure = dataTime['pressure_in']
    windDirection = dataTime['wind_degree']
    location = data['location']['name']
    region = data['location']['region']
    country = data['location']['country']
    value = [temperature, pressure, humidity, windDirection, speed]
    X = dict(zip(features, value))
    df = pd.DataFrame(X, index=[0])
    prediction = model.predict(df)[0]
    return jsonify({
        'Radiation': prediction,
        'Temperature': temperature,
        'Pressure': pressure,
        'Humidity': humidity,
        'WindDirection': windDirection,
        'Speed': speed,
        'location': f"{location}, {region}, {country}",
        'date': dataTime['time'].split(' ')[0],
        'time': dataTime['time'].split(' ')[1],
    })
