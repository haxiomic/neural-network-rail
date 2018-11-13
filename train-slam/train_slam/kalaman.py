import numpy
from filterpy.kalman import MerweScaledSigmaPoints, UnscentedKalmanFilter

from gpscurvature import get_offset_coordinate
from geolocation import load_gpx_file, extract_gps_measurements, create_gpx_file, save_gpx_file

def fx(x, dt):
    [lat, lng, ele, heading, velocity, acceleration] = x
    distance = velocity*dt + 0.5*acceleration*dt**2
    new_velocity = velocity + acceleration*dt
    xs = distance * numpy.sin(heading)
    ys = distance * numpy.cos(heading)
    [new_lat, new_lng] = get_offset_coordinate(lat, lng, xs, ys)
    return numpy.array([ new_lat, new_lng, ele, heading, velocity, acceleration ])

def hx(x):
    return x

def state_mean(sigmas, Wm):
    x = numpy.zeros(6)
    sum_sin, sum_cos = 0., 0.
    for i in range(len(sigmas)):
        s = sigmas[i]
        x[0] += s[0] * Wm[i]
        x[1] += s[1] * Wm[i]
        x[2] += s[2] * Wm[i]
        x[4] += s[4] * Wm[i]
        x[5] += s[5] * Wm[i]
        sum_sin += numpy.sin(s[3])*Wm[i]
        sum_cos += numpy.cos(s[3])*Wm[i]
    x[3] = numpy.arctan2(sum_sin, sum_cos)
    return x

def normalize_angle(angle):
    if angle > numpy.pi:
        angle -= 2*numpy.pi
    if angle < -numpy.pi:
        angle = 2*numpy.pi
    return angle

def residual(a, b):
    x = a - b
    x[3] = normalize_angle(x[3])
    return x

def format_measurement(measurement):
    return [
        measurement.latitude,
        measurement.longitude,
        measurement.elevation,
        measurement.heading,
        measurement.velocity,
        measurement.acceleration,
    ]

dim_x = 6
dim_z = 6
dt = 1

# points=[[0,0,1,1]]
points = MerweScaledSigmaPoints(6, alpha=.1, beta=2., kappa=-1)
kalaman_filter = UnscentedKalmanFilter(dim_x, dim_z, dt, hx, fx, points, x_mean_fn=state_mean, residual_x=residual)

gpx = load_gpx_file('data/track_2018-03-14_134847.gpx')
measurements = list(extract_gps_measurements(gpx))

kalaman_filter.x = numpy.array(format_measurement(measurements[0])) # initial state
kalaman_filter.P *= 0.1 # initial uncertainty
# Standard deviations
lat_lng_std = 0.01
elevation_std = 5
heading_std = numpy.pi/4
velocity_std = 2
acceleration_std = 2
kalaman_filter.R = numpy.diag([
    lat_lng_std**2,
    lat_lng_std**2,
    elevation_std**2,
    heading_std**2,
    velocity_std**2,
    acceleration_std**2,
]) # 1 standard
# kalaman_filter.Q = Q_discrete_white_noise(dim=6, dt=dt, var=0.01**2, block_size=2)

coordinates = []
for measurement in measurements:
    kalaman_filter.predict()
    kalaman_filter.update(format_measurement(measurement))
    [lat, lng, ele, heading, velocity, acceleration] = kalaman_filter.x
    coordinates.append([lat, lng, ele])

gpx = create_gpx_file(coordinates)
save_gpx_file('predict', gpx)