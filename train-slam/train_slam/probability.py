import numpy

from particle import Particle

def calculate_measurement_probability(actual, measured, std_dev):
    """
    actual - actual value (if particle is correct)
    measured - measured value (from GPS reading)
    std_dev - std_dev of measurement
    """
    return numpy.prod(numpy.exp(-(measured - actual)**2/(2*std_dev**2)))

def update_particle_weight_from_measurement(particle, measurement):
    latitude_probability = calculate_measurement_probability(particle.latitude, measurement.latitude, 0.001)
    longitude_probability = calculate_measurement_probability(particle.longitude, measurement.longitude, 0.001)
    velocity_probability = calculate_measurement_probability(particle.velocity, measurement.velocity, 4)
    heading_probability = calculate_measurement_probability(particle.heading, measurement.heading, numpy.pi/8)
    measurement_probability = numpy.prod([
        latitude_probability,
        longitude_probability,
        velocity_probability,
        heading_probability,
    ])
    return Particle(
        particle.latitude,
        particle.longitude,
        particle.velocity,
        particle.heading,
        particle.weight * measurement_probability,
    )

def update_particle_weights_from_measurement(particles, measurement):
    return [
        update_particle_weight_from_measurement(particle, measurement)
        for particle in particles
    ]

def select_population_from_weights(weights):
    number_weights = len(weights)
    summed_weights = numpy.sum(weights)
    normalized_weights = (
        weights / summed_weights
        if summed_weights > 0
        else numpy.arange(number_weights).fill(1/number_weights)
    )
    population_selection = numpy.random.choice(number_weights, number_weights, p=normalized_weights)
    return population_selection


def select_new_particle_population(particles):
    number_particles = len(particles)
    weights = [particle.weight for particle in particles]
    population_selection = select_population_from_weights(weights)
    return [
        Particle(
            particles[i].latitude,
            particles[i].longitude,
            particles[i].velocity,
            particles[i].heading,
            1/number_particles,
        )
        for i in population_selection
    ]