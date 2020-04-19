# -*- coding: utf-8 -*-
"""
Created on 04/04/2020


@author: Paul Festor
"""
import os

from flask import Flask, jsonify, json, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from models.simple_sir import simple_sir
from models.simulator import run_simulator, run_sir_h

# Test master update to deploy 2

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def add(x, y):
    return x + y

# Sample GET request
@app.route('/get_data_sample', methods=["GET"])
def get_data_sample():
    data = {"a": 2, "b": 3}
    return jsonify(data)

# Sample GET request with parameters
@app.route('/get_add_data', methods=["GET"])
def get_add_data():
    input = json.loads(request.args.get('inputFunction'))
    return jsonify({'result': add(input['x'], input['y'])})


# Sample POST request
@app.route('/add_data', methods=["POST"])
def add_data():
    request_data = request.get_json()
    input = request_data['inputFunction']
    x = input["x"]
    y = input["y"]
    result = add(x, y)
    return jsonify({'result': result})

# Sample SIR GET request
@app.route('/get_simple_sir', methods=["GET"])
def get_simple_sir():
    input = json.loads(request.args.get('parameters'))
    print(input)
    s0 = input["s0"]
    lambd = input["lambda"]
    beta = input["beta"]
    data = simple_sir(s0=s0, lambd=lambd, beta=beta)
    return jsonify(data)

# Complex SIR GET request
@app.route('/get_complex_sir', methods=["GET"])
def get_complex_sir():
    input = json.loads(request.args.get('parameters'))
    print(input)

    model = str(input["model"])

    population = int(input["population"])
    lim_time = int(input["lim_time"])
    r0 = input["r0"]

    kpe = input["kpe"]
    krd = input["krd"]
    taux_tgs = input["taux_tgs"]
    taux_thr = input["taux_thr"]
    tem = int(input["tem"])
    tmg = int(input["tmg"])
    tmh = int(input["tmh"])
    thg = int(input["thg"])
    thr = int(input["thr"])
    trsr = int(input["trsr"])

    kmg = taux_tgs
    kmh = 1 - kmg
    kem = r0 / (kmg*tmg + kmh*tmh)
    khr = taux_thr / (1 - taux_tgs)
    if khr > 1:
        khr = 1
    khg = 1 - khr

    krg = 1 - krd

    # model v2
    recovered, exposed, infected, dead, hospitalized, intensive_care, exit_intensive_care, input_recovered, input_exposed, input_infected, input_dead, input_hospitalized, input_intensive_care, input_exit_intensive_care, output_recovered, output_exposed, output_infected, output_dead, output_hospitalized, output_intensive_care, output_exit_intensive_care, = run_simulator(
        model, population, kpe, kem, kmg, kmh, khr, khg, krd, krg, tem, tmg, tmh, thg, thr, trsr, lim_time)

    data = {"recovered": recovered, "exposed": exposed, "infected": infected, "dead": dead,
            "hospitalized": hospitalized, "intensive_care": intensive_care,
            "exit_intensive_care": exit_intensive_care, "input_recovered": input_recovered,
            "input_exposed": input_exposed, "input_infected": input_infected, "input_dead": input_dead,
            "input_hospitalized": input_hospitalized, "input_intensive_care": input_intensive_care,
            "input_exit_intensive_care": input_exit_intensive_care,
            "output_recovered": output_recovered, "output_exposed": output_exposed,
            "output_infected": output_infected, "output_dead": output_dead,
            "output_hospitalized": hospitalized, "output_intensive_care": intensive_care,
            "output_exit_intensive_care": exit_intensive_care, "j_0": input["j_0"]}

    return jsonify(data)


def extract_from_parameters(parameters):
    start_time = int(parameters['start_time'])

    constants_name = ["population", "patient0", "lim_time"]
    delays_name = ['dm_incub', 'dm_r', 'dm_h', 'dm_sm', 'dm_si', 'dm_ss']

    coefficients_name = ['kpe', 'r', 'beta', 'pc_ir', 'pc_ih', 'pc_sm',
                         'pc_si', 'pc_sm_si', 'pc_sm_out', 'pc_si_dc', 'pc_si_out', 'pc_h_ss', 'pc_h_r']

    constants = {key: int(parameters[key]) for key in constants_name}
    delays = {key: int(parameters[key]) for key in delays_name}
    coefficients = {key: parameters[key] for key in coefficients_name}
    return start_time, constants, delays, coefficients

# SIR+H model
# used by 'experiments'
# parameters = {start_time:0, population:xxx, patient0:xxx, ...}
@app.route('/get_sir_h', methods=["GET"])
def get_sir_h():
    parameters = json.loads(request.args.get('parameters'))
    print('get_sir_h', parameters)

    start_time, constants, delays, coefficients = extract_from_parameters(
        parameters)

    rules = sorted(parameters["rules"], key=lambda rule: rule['date'])

    lists = run_sir_h(constants, delays, coefficients, rules)
    return jsonify(lists)


# SIR+H model with timeframe
# parameters= {list:[{start_time:xxx, population:xxx, patient0:xxx, ...}]}
# start_time in (0, 1, 2, 3, ...)
@app.route('/get_sir_h_timeframe', methods=["GET"])
def get_sir_h_timeframe():
    parameters = json.loads(request.args.get('parameters'))
    # print('get_sir_h_timeframe parameters', parameters)
    parameters_list = parameters['list']

    rules = []
    for index, parameters in enumerate(parameters_list):
        if index > 0:
            start_time, constants, delays, coefficients = extract_from_parameters(
                parameters)
            d = {**constants, **delays, **coefficients}
            for key in d:
                rules.append(
                    {'field': key, 'value': d[key], 'date': start_time})

    start_time, constants, delays, coefficients = extract_from_parameters(
        parameters_list[0])
    lists = run_sir_h(constants, delays, coefficients, rules)
    return jsonify(lists)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
