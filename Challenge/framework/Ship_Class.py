import math
from collections import defaultdict

class Ship:
    max_speed = 40 # nautical miles per hour
    min_speed = 2 # nautical miles per hour
    mu_bulker = 3.1 # MAN propulsion manual Table 2.05
    mu_tanker = 3.4 # MAN propulsion manual Table 2.05
    fuel_cons = 1.63 # kg per kw per hour || DESMO
    co2_factor = 3.206 # kg per kg fuel || MAN propulsion manual Table 4.02
    fuel_cons_aux = 100 # kg per hour || DESMO
    c_tanker =  [-2977.4794, 26.8458, 1.3338] # regression model
    c_bulker =  [-1475.4103, 0.0315, 1.9642] # regression model

    def __init__(self, imo, dwt, ship_type='bulker'):
        self.imo: int = imo
        self.dwt: int = dwt
        self.ship_type = ship_type
        self.lats = []
        self.lons = []
        self.timestamps = []
    
    @property
    def n(self):
        return len(self.timestamps)

    @property
    def start_date(self):
        return list(sorted(self.timestamps))[0]
    
    @property
    def end_date(self):
        return list(sorted(self.timestamps))[-1]
    
    @property
    def route_dict(self):
        # {pd.datetime: {lat: 0.0, lon: 0.0}}
        if not hasattr(self, '_route_dict'):
            rd = {}
            for i, t in enumerate(self.timestamps):
                rd[t] = {
                    'lon': self.lons[i], 
                    'lat': self.lats[i]
                }
            dates = sorted(list(rd.keys()))
            rd = {d : rd[d] for d in dates}
            self._route_dict = rd
            self.add_dist_speed()
        return self._route_dict
    
    def add_dist_speed(self):
        rd = self.route_dict
        dates = list(rd.keys())
        pts = list(rd.values())
        for i, d in enumerate(dates):
            if i == 0:
                dist = 0
                speed = 0
                time = 0
            else:
                dist = self.dist(pts[i], pts[i-1]) # nautical miles
                time = (dates[i] - dates[i-1]).seconds / 3600 # hours
                speed = dist / (time) # knots
            rd[d]['dist'] = dist
            rd[d]['speed'] = round(speed, 2)
            rd[d]['time'] = round(time, 2)
        self._route_dict = rd

    def add_fuel_and_co2(self):
        rd = self.route_dict
        for d, p in rd.items():
            t = p['time']
            s = p['speed']
            power = self.power_required(s)
            f_main, f_aux, co2_main, co2_aux = self.cons_emissions(power, t)
            rd[d]['power'] = round(power,1)
            rd[d]['fuel_cons_main'] = round(f_main,1)
            rd[d]['fuel_cons_aux'] = round(f_aux,1)
            rd[d]['co2_main'] = round(co2_main,1)
            rd[d]['co2_aux'] = round(co2_aux,1)
        self._route_dict = rd
        
                
    def prune_outliers(self):
        rd = self.route_dict
        keys = list(rd.keys())
        for k in keys:
            if rd[k]['speed'] > self.max_speed:
                del rd[k]
        self._route_dict = rd


    
    @property
    def geoJson(self):
        rd = self.route_dict
        coords = [[p['lon'], p['lat']] for p in rd.values()]
        geoJ = {
            "geometry": {
                "coordinates": coords,
                "type": "LineString"
                },
            "properties": {},
            "type": "Feature"
            }
        return geoJ

    @property
    def voyage_statistics(self):
        rd = self.route_dict
        st = defaultdict(float) # statistics
        st['imo'] = self.imo
        st['dwt'] = self.dwt
        for p in rd.values():
            st['voyage_distance'] += p['dist']
            st['total_fuel_cons_main'] += p['fuel_cons_main']
            st['total_fuel_cons_aux'] += p['fuel_cons_aux']
            st['total_co2_main'] += p['co2_main']
            st['total_co2_aux'] += p['co2_aux']
            st['voyage_hours'] += p['time']
            if p['speed'] > self.min_speed:
                st['steaming_hours'] += p['time']
            else:
                st['harbor_hours'] += p['time']
        st['avg_steaming_speed'] = st['voyage_distance'] / max(st['steaming_hours'], 1)
        st['total_tons_fuel'] = (st['total_fuel_cons_main'] + st['total_fuel_cons_aux']) / 1000
        st['total_tons_co2'] = (st['total_co2_main'] + st['total_co2_aux']) / 1000
        st['avg_daily_tons_fuel'] = st['total_tons_fuel'] / st['voyage_hours'] * 24
        st['avg_daily_tons_co2'] = st['total_tons_co2'] / st['voyage_hours'] * 24
        out_statistics = {
            'ship_type' : self.ship_type,
            'imo' : self.imo,
            'dwt' : self.dwt,
            'voyage_start_date' : str(self.start_date)[:10],
            'voyage_end_date' : str(self.end_date)[:10]
            }
        for k, v in st.items():
            out_statistics[k] = round(v, 1)
        return out_statistics

    def power_required(self, s):
        # return power in kw
        if self.ship_type == 'tanker':
            c = self.c_tanker
            mu = self.mu_tanker
        if self.ship_type == 'bulker':
            c = self.c_bulker
            mu = self.mu_bulker
        return c[0] + c[1] * self.dwt + c[2] * s**mu # kw

    def cons_emissions(self, kw, t):
        # t = time (hours)
        fuel_cons_main = self.fuel_cons * kw * t # kg
        fuel_cons_aux = self.fuel_cons_aux * t # kg
        co2_main = fuel_cons_main * self.co2_factor # kg
        co2_aux = fuel_cons_aux * self.co2_factor # kg
        return fuel_cons_main, fuel_cons_aux, co2_main, co2_aux

    def dist(self, pt1, pt2):
        '''
        Returns:
        Distance between two stations IN KILOMETERS
        '''
        lon1, lat1 = pt1['lon'], pt1['lat']
        lon2, lat2 = pt2['lon'], pt2['lat']

        R = 6371e3  # radius of earth in meters
        phi1 = lat1 * math.pi / 180  # phi and lambda in radians
        phi2 = lat2 * math.pi / 180
        delta_phi = phi2 - phi1
        delta_lambda = (lon2 - lon1) * math.pi / 180

        a = (
            (math.sin(delta_phi/2))**2 +
            math.cos(phi1) * math.cos(phi2) *
            (math.sin(delta_lambda/2))**2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        distance = R * c  # in meters
        distance *= .5399568 / 1000 # in nautical miles

        return round(distance, 2)