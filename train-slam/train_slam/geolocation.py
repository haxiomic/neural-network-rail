import gpxpy
import gpxpy.gpx

from gpscurvature import get_distance, get_initial_bearing
from utilities import write_csv

def find_distance(previous_point, current_point):
    return get_distance(previous_point.latitude, previous_point.longitude, current_point.latitude, current_point.longitude)

def find_heading(previous_point, current_point):
    return get_initial_bearing(previous_point.latitude, previous_point.longitude, current_point.latitude, current_point.longitude)

def load_gpx_file(filename):
    with open(filename) as gpx_file:
        return gpxpy.parse(gpx_file)

def print_attributes(object):
    for attr in dir(object):
        print(attr)

def print_point(point):
    print('point.latitude', point.latitude)
    print('point.longitude', point.longitude)
    print('point.time', point.time)

class Measurement:
    def __init__(self, latitude, longitude, elevation, heading, velocity, acceleration, timedelta):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.heading = heading
        self.velocity = velocity
        self.acceleration = acceleration
        self.timedelta = timedelta
    def json(self):
        return {
            key: getattr(self, key)
            for key in ['latitude', 'longitude', 'elevation', 'heading', 'velocity', 'acceleration', 'timedelta']
        }

def extract_gps_measurements(gpx, not_moving_threshold=0.1):
    """
    find velocity and heading for all measurements
    loop through measurements until there is a motion
    """
    previous_velocity = 0
    previous_point = gpx.tracks[0].segments[0].points[0]
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                distance = find_distance(previous_point, point)
                timedelta = point.time_difference(previous_point)
                if (distance > not_moving_threshold):
                    heading = find_heading(previous_point, point)
                    velocity = distance / timedelta
                    acceleration = velocity - previous_velocity
                    previous_velocity = velocity
                    yield Measurement(
                        point.latitude,
                        point.longitude,
                        point.elevation,
                        heading,
                        velocity,
                        acceleration,
                        timedelta
                    )
                previous_point = point

def create_gpx_file(coordinates):
    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    # Add all coordinates
    for coordinate in coordinates:
        point = gpxpy.gpx.GPXTrackPoint(coordinate[0], coordinate[1], elevation=coordinate[2])
        gpx_segment.points.append(point)
    return gpx

def save_gpx_file(name, gpx):
    with open('./data/{}.gpx'.format(name), 'w') as open_file:
        open_file.write(gpx.to_xml())

def write_measurements_to_csv(name, measurements):
    rows = [
        ['latitude', 'longitude', 'velocity', 'heading']
    ] + [
        [measurement.latitude, measurement.longitude, measurement.velocity, measurement.heading]
        for measurement in measurements
    ]
    write_csv(name, rows)

# if (__name__ == "__main__"):
#     name = 'track_2018-03-14_134847'
#     gpx = load_gpx_file('data/{}.gpx'.format(name))
#     measurements = extract_gps_measurements(gpx)
#     write_measurements_to_csv(name, measurements)
#     for measurement in list(measurements)[:10]:
#         print(measurement.latitude, measurement.longitude, measurement.velocity, measurement.heading)