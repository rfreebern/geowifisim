from time import time as timestamp
from math import radians, sin, cos, asin, sqrt

from flask import Flask, request, render_template

from gpolyline_decoder import decode_line

app = Flask(__name__)

# Haversine great circle distance formula
def distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a)) 
    return c * 6367 # kilometers

def get_speed(term):
    # Speeds in KPH
    SPEED = {
        'STROLLING': 3,
        'WALKING': 5,
        'JOGGING': 8,
        'RUNNING': 10,
        'BIKING': 20,
        'BICYCLING': 20,
        'CRUISING': 50,
        'DRIVING': 100,
        'FLYING': 950
    }

    if term.upper() in SPEED:
        speed = SPEED[term.upper()]
    else:
        speed = SPEED['WALKING']
    return speed

def calculate_position(start, path, speed):
    # Convert speed to m/s
    speed = speed * 1000 / 3600

    # Elapsed time since start
    elapsed = time() - start

    # Total distance traveled so far (constant speed)
    distance_traveled = speed * elapsed

    previous_point = path[0]
    total_distance = 0
    position = path[-1]
    for point in path[1:]:
        distance_between = distance(previous_point[1], previous_point[0],
                                    point[1], point[0]) * 1000
        if total_distance + distance_between >= distance_traveled:
            # This is the path segment we're on.
            distance_on_segment = distance_traveled - total_distance
            lat_step = (point[0] - previous_point[0]) / distance_between
            lon_step = (point[1] - previous_point[1]) / distance_between
            position = (previous_point[0] + (lat_step * distance_on_segment),
                        previous_point[1] + (lon_step * distance_on_segment))
        else:
            total_distance += distance_between
    return position

@app.route('/')
def home():
    start = request.args.get('start', None)
    path = request.args.get('path', None)
    speed = request.args.get('speed', 'WALKING')

    if start and path:
        try:
            start = date.fromtimestamp(start)
        except TypeError:
            abort(400)

        try:
            path = decode_line(path)
        except IndexError:
            abort(400)

        speed = get_speed(speed)

        position = calculate_position(start, path, speed)
        response = make_response(render_template('location.json',
            position=position))
        response.headers['Content-type'] = 'text/json'
    elif not request.args.length():
        response = make_response(render_template('index.html'))
    else:
        abort(400)
    return response

if __name__ == "__main__":
    app.run()
