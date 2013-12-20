'''
This modules exposes geometry data for Unites States. It exposes a dictionary 'data' which is
indexed by the two letter state code (e.g., 'CA', 'TX') and has the following dictionary as the
associated value:

    data['CA']['name']
    data['CA']['region']
    data['CA']['lats']
    data['CA']['lons']

'''
import csv
import codecs
import gzip
import xml.etree.cElementTree as et
from os.path import dirname, join

nan = float('NaN')

data = {}
with gzip.open(join(dirname(__file__), 'US Regions State Boundaries.csv.gz')) as f:
    decoded = codecs.iterdecode(f, "utf-8")
    next(decoded)
    reader = csv.reader(decoded, delimiter=',', quotechar='"')
    for row in reader:
        region, name, code, geometry, dummy = row
        xml = et.fromstring(geometry)
        lats = []
        lons = []
        for i, poly in enumerate(xml.findall('.//outerBoundaryIs/LinearRing/coordinates')):
            if i > 0:
                lats.append(nan)
                lons.append(nan)
            coords = (c.split(',')[:2] for c in poly.text.split())
            lat, lon = list(zip(*[(float(lat), float(lon)) for lon, lat in
                coords]))
            lats.extend(lat)
            lons.extend(lon)
        data[code] = {
            'name'   : name,
            'region' : region,
            'lats'   : lats,
            'lons'   : lons,
        }
