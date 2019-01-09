#!/usr/bin/env python
# coding: utf-8

import numpy
import pandas
import geopandas
import matplotlib.pyplot
from shapely.geometry import Point, LineString, Polygon
from convertbng.util import convert_lonlat

railways_pickle_path = './data/lat_lng_railways.pkl'

def create_bounding_polygon(bbox):
    
    p1 = Point(bbox[0], bbox[3])
    p2 = Point(bbox[2], bbox[3])
    p3 = Point(bbox[2], bbox[1])
    p4 = Point(bbox[0], bbox[1])

    np1 = (p1.coords.xy[0][0], p1.coords.xy[1][0])
    np2 = (p2.coords.xy[0][0], p2.coords.xy[1][0])
    np3 = (p3.coords.xy[0][0], p3.coords.xy[1][0])
    np4 = (p4.coords.xy[0][0], p4.coords.xy[1][0])

    return Polygon([np1, np2, np3, np4])

def convert_linestring(linestring):
    [eastings, northings] = list(numpy.array(linestring.coords).transpose())
    return LineString(numpy.array(convert_lonlat(eastings, northings)).transpose())

def generate_railway_linstrings():

    railways_file_path = './data/osm_railway.shp'
    railways = geopandas.GeoDataFrame.from_file(railways_file_path)

    # convert lat_lng does not work when northings or eastings are negative (infinite loop)
    railways_filter = railways.geometry.apply(lambda linestring: all([(x > 0 and y > 0) for (x, y) in linestring.coords]))
    filtered_railways = railways[railways_filter]

    # convert all railways to latitude longitude
    railways_geometry = [convert_linestring(linestring) for linestring in railways.geometry]
    lat_lng_railways = geopandas.GeoDataFrame(railways.copy(), geometry=railways_geometry)
    lat_lng_railways.to_pickle(railways_pickle_path)

def plot_track_and_railways(gpx_route_filename):

    # Could not be bothered to use regex
    track_id = gpx_route_filename.split('_')[-1].split('.')[0]
    output_name = 'railways__filtered--{}'.format(track_id)

    # Pickled data has been added to the repository as takes some time to create
    railways = geopandas.GeoDataFrame(pandas.read_pickle(railways_pickle_path))

    train_route = geopandas.read_file(gpx_route_filename, layer='track_points')
    bounding_polygon = create_bounding_polygon(train_route.total_bounds)

    # For some reason a later line string is corrupted
    valid_entries = 40660
    # TODO: filter out corrupted linstrings (need to work out how firstly)
    intersection = railways.geometry.head(valid_entries).intersects(bounding_polygon)
    filtered_railways = railways.head(valid_entries)[intersection]

    # Store the filtered track data in GeoJSON
    filtered_railways.to_file('./data/{}.json'.format(output_name), 'GeoJSON')

    axis = geopandas.GeoSeries(bounding_polygon).plot(color='red')
    filtered_railways.plot(color='black', linewidth=0.6, ax=axis)
    train_route.plot(color='blue', markersize=0.6, ax=axis)

    # matplotlib.pyplot.show()
    matplotlib.pyplot.savefig('./data/{}.svg'.format(output_name), transparent=True)

def main():
    # generate_railway_linstrings()
    plot_track_and_railways('./data/track_2018-03-14_134847.gpx')

if (__name__ == "__main__"):
    main()