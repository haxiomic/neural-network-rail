import datetime
import xmltodict

__author__ = "David George Hopes"

def importGPX(filepath):
    """
    Imports GPS data from .gpx file, returns list of python dicts

    @param filepath: the absolute or relative filepath of the gpx
    @return: list of python dicts containing GPS data
    """
    with open(filepath) as infile:
        gps_data = xmltodict.parse(infile.read())

    intervals = []
    for i in gps_data['gpx']['trk']['trkseg']['trkpt']:
        interval = {}
        interval['latitude'] = float(i['@lat'])
        interval['longitude'] = float(i['@lon'])
        interval['time'] = datetime.datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%SZ")
        try:
            for offset in i['extensions']['gpxacc:AccelerationExtension']['gpxacc:accel']:
                interval['time'] = interval['time']+datetime.timedelta(milliseconds=int(offset['@offset']))
                interval['x'] = float(offset['@x'])
                interval['y'] = float(offset['@y'])
                interval['z'] = float(offset['@z'])
                intervals.append(interval)
        except KeyError:
            print('Error importing: {}'.format(offset))
    
    # TODO return more efficient data structure
    return intervals