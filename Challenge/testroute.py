import searoute as sr
import folium


# Define origin and destination points:
origin = [0.3515625, 50.064191736659104] #[long, lat]

destination = [117.42187500000001, 39.36827914916014]

origin = [5.3, 43.3] # marseille
origin = [-90.254244,30.162523] # new orleans
destination = [-74.1,40.7] # new york


# folium.GeoJson(antarctic_ice_edge, name="geojson").add_to(m)



route = sr.searoute(origin, destination)
# # > Returns a GeoJSON LineString Feature
# # show route distance with unit
print("{:.1f} {}".format(
    route.properties['length'], route.properties['units']))

# # Optionally, define the units for the length calculation included in the properties object.
# # Defaults to km, can be can be 'm' = meters 'mi = miles 'ft' = feets 'in' = inches 'deg' = degrees
# # 'cen' = centimeters 'rad' = radians 'naut' = nauticals 'yd' = yards
routeMiles = sr.searoute(origin, destination, units="naut")
print(routeMiles)
# points = [origin] + routeMiles.geometry.coordinates + [destination]


fmap = folium.Map(location=[40,-95], zoom_start = 2)

print(routeMiles)

folium.GeoJson(routeMiles).add_to(fmap)

fmap.save("mymap.html")