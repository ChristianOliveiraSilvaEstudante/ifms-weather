from flask import *
import hashlib
import hmac
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/weather", methods=['POST'])
def weather():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')

    sharedSecret = "abcdef"
    query = f"/packages/basic-1h?lat=47.1&lon=8.6&apikey=LGO2DyVrPRco7Ul0&lat={lat}&lon={lon}&asl=279&format=json"

    sig = hmac.new(sharedSecret.encode(), query.encode(), hashlib.sha256).hexdigest()
    signedUrl = f"https://my.meteoblue.com{query}&sig={sig}"

    res = requests.get(signedUrl)

    if res.status_code == 200:
        json_data = res.json()

        return {
            "temperature": json_data['data_1h']['temperature'][0],
            "felttemperature": json_data['data_1h']['felttemperature'][0],
            "windspeed": json_data['data_1h']['windspeed'][0],
            "relativehumidity": json_data['data_1h']['relativehumidity'][0],
            "sealevelpressure": json_data['data_1h']['sealevelpressure'][0],
            "uvindex": json_data['data_1h']['uvindex'][0],
        }

    return {}