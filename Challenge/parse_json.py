import json
import pandas as pd
import folium
import os
from framework.Ship_Class import Ship

####################################################
# ship reports files
report_files = [
    # 'ship_voyage_reports/BC_9135652.json',
    'ship_voyage_reports/BC_9456240.json',
    'ship_voyage_reports/BC_9472696.json',
    'ship_voyage_reports/BC_9710048.json',
    'ship_voyage_reports/BC_9939333.json',
    'ship_voyage_reports/T_9144914.json',
    'ship_voyage_reports/T_9277785.json',
    'ship_voyage_reports/T_9326641.json',
    'ship_voyage_reports/T_9418054.json',
    'ship_voyage_reports/T_9475430.json',
    ]

####################################################


def json_print(data, name=''):
    # prints dictionary data in a nice readable format
    data = {str(d): data[d] for d in data}
    print(f'{name} = ', json.dumps(data, indent=4), '\n')


def get_reports(filename):
    # load all reports contained in ais hourly json
    with open(filename, 'r') as f:
        reports = json.load(f)['results']
    return reports

def add_reports_json_to_ships_dict(ships_dict, json_filename):
    reports = get_reports(json_filename)
    print(f'{len(reports)} reports found in file: {json_filename}')
    ship_type = 'bulker'
    if 'T' in json_filename:
        ship_type = 'tanker'
    for r in reports:
        imo = r['imo']
        lat = float(r['ais_lat'])
        lon = float(r['ais_lon'])
        if imo not in ships_dict:
            s = Ship(imo=imo, dwt=r['dwt'], ship_type=ship_type)
            s.lats.append(lat)
            s.lons.append(lon)
            s.timestamps.append(pd.to_datetime(r['position_timestamp']))
            ships_dict[imo] = s
        else:
            ships_dict[imo].lats.append(lat)
            ships_dict[imo].lons.append(lon)
            ships_dict[imo].timestamps.append(pd.to_datetime(r['position_timestamp']))
    return ships_dict


ships = {}
for filename in report_files:
    reports = add_reports_json_to_ships_dict(ships, filename)

for s in ships.values():
    print(f'ship_imo = {s.imo},  n_waypoints = {s.n}')

for ship in ships.values():
    input('press enter to continue: ')
    ship.prune_outliers()
    ship.add_fuel_and_co2()

    rd = ship.route_dict
    # rd = {str(d): rd[d] for d in rd}
    voyage_statistics = ship.voyage_statistics
    # json_print(rd)
    json_print(voyage_statistics)
    route = ship.geoJson

    fmap = folium.Map(location=[0,0], zoom_start = 2)


    folium.GeoJson(route).add_to(fmap)

    fmap.save("new_map.html")
    os.system('open new_map.html')
