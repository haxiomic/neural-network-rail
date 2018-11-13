import csv
import glob
import os.path

def yield_route_assets():
    routes = {}
    last_route = ''
    for asset_path in glob.glob('/Volumes/USB Disk/*/*/*.jpg'):
        route = os.path.dirname(asset_path).split('/')[-2]
        asset = os.path.basename(asset_path)
        routes[route] = routes.get(route, [])
        routes[route].append(asset)
        if (last_route != route and last_route != ''):
            yield (last_route, routes[last_route])
        last_route = route

def write_csv_file(name, assets):
    filepath = 'data/{}.csv'.format(name)
    with open(filepath, 'w') as open_file:
        csv_file = csv.writer(open_file)
        csv_file.writerows([
            ['Asset Name', 'Description']
        ] + [
            [asset, '']
            for asset in assets
        ])

def store_route_csv_files(route_assets):
    for route, assets in route_assets:
        print(route, len(assets))
        write_csv_file(route, assets)

if (__name__ == "__main__"):
    route_assets = yield_route_assets()
    store_route_csv_files(route_assets)