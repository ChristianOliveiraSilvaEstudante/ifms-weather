from flask import *
import hashlib
import hmac
import requests
from sqlalchemy import create_engine, Column, Float, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///search_database.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class Search(Base):
    __tablename__ = 'search'

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)
    lon = Column(Float)
    temperature = Column(Float)
    felttemperature = Column(Float)
    windspeed = Column(Float)
    relativehumidity = Column(Float)
    sealevelpressure = Column(Float)
    uvindex = Column(Integer)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

app = Flask(__name__)

@app.route("/")
def hello_world():
    results = db.query(Search).all()
    return render_template('index.html', results=results)

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

        temperature = json_data['data_1h']['temperature'][0]
        felttemperature = json_data['data_1h']['felttemperature'][0]
        windspeed = json_data['data_1h']['windspeed'][0]
        relativehumidity = json_data['data_1h']['relativehumidity'][0]
        sealevelpressure = json_data['data_1h']['sealevelpressure'][0]
        uvindex = json_data['data_1h']['uvindex'][0]

        new_search = Search(lat=lat, lon=lon, temperature=temperature, felttemperature=felttemperature, windspeed=windspeed, relativehumidity=relativehumidity, sealevelpressure=sealevelpressure, uvindex=uvindex)
        db.add(new_search)
        db.commit()

        return {
            "temperature": temperature,
            "felttemperature": felttemperature,
            "windspeed": windspeed,
            "relativehumidity": relativehumidity,
            "sealevelpressure": sealevelpressure,
            "uvindex": uvindex,
        }

    return {}