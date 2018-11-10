import math

__author__ = "David George Hopes"

def get_distance(latitude1, longitude1, latitude2, longitude2):
    """
    Uses the Haversine formula with the mean Earth radius, accurate enough for
    smaller distances
    
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
    print("phi1: {}".format(phi1))

    phi2 = math.radians(latitude2) 
    print("phi2: {}".format(phi2))
    
    #
    delta_phi_degrees = latitude2 - latitude1
    print("delta_phi_degrees: {}".format(delta_phi_degrees))
    delta_phi = math.radians(delta_phi_degrees)
    print("delta_phi: {}".format(delta_phi))
    delta_lambda_degrees = longitude2 - longitude1
    print("delta_lambda_degrees: {}".format(delta_lambda_degrees))
    delta_lambda = math.radians(delta_lambda_degrees)
    print("delta_lambda: {}".format(delta_lambda))
    
    a = math.sin(delta_phi/2.0)**2.0 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2.0)**2.0
    print("a: {}".format(a))
    
    c = 2.0*math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    print("c: {}".format(c))


    distance = radius * c
    
    return distance