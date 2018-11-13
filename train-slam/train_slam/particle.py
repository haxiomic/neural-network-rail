import numpy

from gpscurvature import get_offset_coordinate

class Particle:
    def __init__(self, latitude, longitude, velocity, heading, weight):
        self.latitude = latitude
        self.longitude = longitude
        self.velocity = velocity
        self.heading = heading
        self.weight = weight
    def __repr__(self):
        return "({},{}) {}m/s @{} {}/1".format(self.latitude, self.longitude, self.velocity, self.heading, self.weight) 

def generate_particles(number_particles, latitude, longitude, velocity=0, heading=0):
    return [
        Particle(latitude, longitude, velocity, heading, 1/number_particles)
        for i in range(number_particles)
    ]

def find_offset(heading, theta, radius, direction):
    straight_line_distance = radius * numpy.sqrt(2 - 2 * numpy.cos(theta))
    angle_from_heading = direction * (numpy.pi - theta) / 2
    straight_line_angle = heading + angle_from_heading
    return [
        straight_line_distance * numpy.cos(straight_line_angle),
        straight_line_distance * numpy.sin(straight_line_angle),
    ]

def move_particle_radius(particle, acceleration, radius, direction, time):
    """Moves particle to new position given acceleration over time"""
    distance = particle.velocity*time + 0.5*acceleration*time**2
    velocity = particle.velocity + acceleration*time
    theta = direction * distance / radius
    heading = particle.heading + theta
    print('distance', distance, 'velocity', velocity, 'theta', theta, 'heading', heading)
    [xs, ys] = find_offset(particle.heading, theta, radius, direction)
    [latitude, longitude] = get_offset_coordinate(particle.latitude, particle.longitude, xs, ys)
    return Particle(
        latitude,
        longitude,
        velocity,
        heading,
        particle.weight,
    )

def move_particle(particle, acceleration, theta, time):
    """Moves particle to new position given acceleration over time"""
    distance = particle.velocity*time + 0.5*acceleration*time**2
    velocity = particle.velocity + acceleration*time
    heading = (particle.heading + theta) % 2*numpy.pi
    print('distance', distance, 'velocity', velocity, 'theta', theta, 'heading', heading)
    xs = distance * numpy.sin(heading)
    ys = distance * numpy.cos(heading)
    [latitude, longitude] = get_offset_coordinate(particle.latitude, particle.longitude, xs, ys)
    return Particle(
        latitude,
        longitude,
        velocity,
        heading,
        particle.weight,
    )

def find_next_acceleration(particle, min_acceleration=-1.2, median_acceleration=0, max_acceleration=0.8):
    acceleration_range = max_acceleration - min_acceleration
    standard_deivation = acceleration_range / 6
    return numpy.random.normal(median_acceleration, standard_deivation)

def find_next_radius(particle, min_radius=70, median_radius=1000, max_radius=10000):
    radius_range = max_radius - min_radius
    standard_deivation = radius_range / 6
    return numpy.random.normal(min_radius+radius_range/2, standard_deivation)

def find_next_theta(particle, min_theta=-numpy.pi/8, median_theta=0, max_theta=numpy.pi/8):
    theta_range = max_theta - min_theta
    standard_deivation = theta_range / 6
    return numpy.random.normal(median_theta, standard_deivation)

def find_next_direction(particle):
    return numpy.random.choice([-1, 1])

def randomly_move_particle_radius(particle, time):
    acceleration = find_next_acceleration(particle) #, min_acceleration, median_acceleration, max_acceleration)
    radius = find_next_radius(particle) #, min_radius, median_radius, max_radius)
    direction = find_next_direction(particle)
    return move_particle(particle, acceleration, radius, direction, time)

def randomly_move_particle(particle, time):
    acceleration = find_next_acceleration(particle)
    theta = find_next_theta(particle)
    return move_particle(particle, acceleration, theta, time)

def randomly_move_particles(particles, time):
    return [
        randomly_move_particle(particle, time)
        for particle in particles
    ]

def get_objects_attr(objects, attr):
    return [
        getattr(obj, attr)
        for obj in objects
    ]

def get_average_object_attr(objects, attr):
    return numpy.average(get_objects_attr(objects, attr), axis=0)

def calculate_average_particle(particles):
    return Particle(
        get_average_object_attr(particles, 'latitude'),
        get_average_object_attr(particles, 'longitude'),
        get_average_object_attr(particles, 'velocity'),
        get_average_object_attr(particles, 'heading'),
        sum(get_objects_attr(particles, 'weight')),
    )

def print_particles(particles):
    for particle in particles:
        print(particle)