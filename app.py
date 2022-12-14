import flask
import pickle
import pandas as pd
import numpy as np
from datetime import date
from flask import Flask, request, render_template, jsonify

import asyncio
import os
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

pipe = pickle.load(
    open('models/cropmodel.pkl', 'rb'))


@app.route('/')
def home():
    return 'hi'


@app.route('/predict', methods=['POST'])
def predict():
    # https://www.ncei.noaa.gov/cag/global/time-series/globe/land_ocean/ytd/7/2012-2022

    country = flask.request.json
    country = country['country']['label']

    # country = request.args.get('country')
    # country = flask.request.json
    # country = country['country']['label']

    # country = flask.request.country

    def run_model(year_subtraction, item):
        d = {'Area': [country], 'Item': [item], 'Year': [2013-year_subtraction], 'average_rain_fall_mm_per_year': [
            1000.0], 'pesticides_tonnes': [3000-year_subtraction*100], 'avg_temp': [20.54262658451951]}

        test = pd.DataFrame(data=d)
        prediction = pipe.predict(test)

        return prediction[0]

    crops = ['Maize', 'Sweet potatoes', 'Wheat', 'Cassava', 'Potatoes',
             'Rice, paddy', 'Sorghum', 'Soybeans', 'Yams',
             'Plantains and others']

    total = 0.0
    answ = [[], [], []]

    for i in range(len(crops)):
        crop = crops[i]

        current = run_model(0, crop)
        last_5 = run_model(10, crop)
        last_30 = run_model(30, crop)

        answ[0].append(min(int((current-last_5)*100/last_5), 350))
        answ[1].append(min(int((current-last_30)*100/last_30), 350))

        total += (min(int((current-last_5)*100/last_5), 350))

    for i in range(len(crops)):
        answ[2].append(min(int((answ[0][i]+total/10)*3), 350))

    # comparison to last 5 years for that crop worldwide (2013)

    # comparison to last 30 years for that crop worldwide
    print(answ)
    return answ


if __name__ == "__main__":
    app.run()
