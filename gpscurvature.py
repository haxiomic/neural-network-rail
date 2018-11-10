import math

__author__ = "David George Hopes"

def get_distance(latitude1, longitude1, latitude2, longitude2):
    """
    Uses the Haversine formula with the mean Earth radius, accurate enough for
    smaller distances.
    
    @param latitude1: the latitude of point 1, in degrees
    @param longitude1: the latitude of point 1, in degrees
    @param latitude2: the longitude of point 2, in degrees
    @param longitude2: the longitude of point 2, in degrees
    @return: distance between two points, in metres
    """
    # mean earth radius in metres
    radius = 6373000
    
    # latitude and longitude measured in degrees, convert to radians
    phi1 = math.radians(latitude1)
    phi2 = math.radians(latitude2) 
    
    # calculate deltas in degrees, convert to radians
    delta_phi = math.radians(latitude2 - latitude1)
    delta_lambda = math.radians(longitude2 - longitude1)
    
    a = math.sin(delta_phi/2.0)**2.0 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2.0)**2.0
    
    c = 2.0*math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    distance = radius * c
    
    return distance

def get_initial_bearing(start_latitude, start_longitude, end_latitude, end_longitude):
    """
    Uses the Haversine formula with the mean Earth radius to calculate the initial bearing from point 1, accurate enough for
    smaller distances.
    
    @param start_latitude: the latitude of point 1, in degrees
    @param start_longitude: the latitude of point 1, in degrees
    @param end_latitude: the longitude of point 2, in degrees
    @param end_longitude: the longitude of point 2, in degrees
    @return: distance between two points, in metres
    """
    phi1 = math.radians(start_latitude)
    phi2 = math.radians(end_latitude) 

    delta_lambda = math.radians(end_longitude - start_longitude)

    y = math.sin(delta_lambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) *math.cos(delta_lambda)

    bearing_radians = math.atan2(y, x)
    bearing_degrees = math.degrees(bearing_radians)

    return bearing_degrees