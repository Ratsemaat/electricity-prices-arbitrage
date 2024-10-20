from flask import Flask, request
from recommendation_algorithm import EnergyProfile, Battery, PricesData
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/mock")
def hello_world():
    return "Hellasdo, World!"


@app.route("/get-recommendation")
def hello_world():
    consumption_profile = request.args.get('consumption_profile')
    profile = EnergyProfile()

    for profile_hour in consumption_profile:
        profile.add_entry(profile_hour.timestamp, profile_hour.estimated_kW_consumption)


    battery_level = request.args.get('battery_level')
    min_battery_level = request.args.get('battery_level')
    max_battery_level = request.args.get('battery_level')
    bandwidth = request.args.get('bandwidth')
    efficiency = request.args.get('efficiency')
    network_fee = request.args.get('network_fee')
    stock_electricity_prices = request.args.get('stock_electricity_prices')
    
    prices = PricesData()


    for prices_hour in stock_electricity_prices:
        profile.add_entry(prices_hour.timestamp, prices_hour.price)

    battery = Battery(len(profile.get_future_data()), bandwidth, bandwidth)
    battery.set_objective(prices.get_future_data().map(lambda l: l['price'],  network_fee, profile.get_future_data().map(lambda l: l['consumption_in_kWh'])))
    
    battery.add_storage_constraints(efficiency, min_battery_level, max_battery_level, battery_level)
    battery.solve_model()
    
    a = battery.collect_output()


