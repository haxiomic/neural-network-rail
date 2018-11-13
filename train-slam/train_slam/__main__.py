import numpy

from plotter import Plotter
from particle import generate_particles, randomly_move_particles, print_particles, calculate_average_particle
from probability import update_particle_weights_from_measurement, select_new_particle_population
from geolocation import load_gpx_file, extract_gps_measurements, create_gpx_file, save_gpx_file
from utilities import read_csv

def run_single_iteration():
    print("generate_particles")
    particles = generate_particles(10)
    print_particles(particles)
    print("find_next_particles")
    particles = find_next_particles(particles, 1)
    print_particles(particles)
    print("update_particle_weights_from_acceleration", [0.1, 0])
    particles = update_particle_weights_from_acceleration(particles, [0.1, 0])
    print_particles(particles)

def plot_particle_measurement_updates(plotter, measurement, particles):
    plotter.append_to_line([ measurement.longitude, measurement.latitude ])
    longitudes = [particle.longitude for particle in particles]
    latitudes = [particle.latitude for particle in particles]
    plotter.change_points([ longitudes, latitudes ])
    plotter.draw_updates()

def run_full_track():
    plotter = Plotter()
    number_particles = 10
    gpx = load_gpx_file('data/track_2018-03-14_134847.gpx')
    measurements = list(extract_gps_measurements(gpx))
    particles = generate_particles(
        number_particles,
        measurements[0].latitude,
        measurements[0].longitude,
        measurements[0].velocity,
        measurements[0].heading,
    )
    # Simulation to run
    for measurement in measurements:
        # Move the particles randomly given acceleration std deviation around zero
        particles = randomly_move_particles(particles, measurement.timedelta)
        # Next we will add the measurement information to the particles
        particles = update_particle_weights_from_measurement(particles, measurement)
        # Finally we randomly select highest weights
        particles = select_new_particle_population(particles)
        # Plot the measurements and latest particles
        plot_particle_measurement_updates(plotter, measurement, particles)
        print_particles(particles)
        # Take input to wait for next
        input('Next step?')

def test_particle_motion():
    plotter = Plotter()
    number_particles = 10
    gpx = load_gpx_file('data/track_2018-03-14_134847.gpx')
    measurements = list(extract_gps_measurements(gpx))
    particles = generate_particles(
        number_particles,
        measurements[0].latitude,
        measurements[0].longitude,
        measurements[0].velocity,
        measurements[0].heading,
    )
    for measurement in measurements:
        average_particle = calculate_average_particle(particles)
        plot_particle_measurement_updates(plotter, average_particle, particles)
        particles = randomly_move_particles(particles, measurement.timedelta)
        input('Next step?')

def parse_accurate_csv_file():
    coordinates = []
    rows = read_csv('london_vic_railstrings')
    for row in rows[1:]:
        [lng_l, lat_l, ele_l, lng_r, lat_r, ele_r] = map(float, row)
        coordinates.append([
            0.5*(lng_r + lng_l),
            0.5*(lat_r + lat_l),
            0.5*(ele_r + ele_l),
        ])
    gpx = create_gpx_file(coordinates)
    save_gpx_file('perfect', gpx)


if (__name__ == "__main__"):
    # run_full_track()
    # test_particle_motion()
    parse_accurate_csv_file()