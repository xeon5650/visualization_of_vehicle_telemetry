import pandas as pd
import folium
import branca
import geopandas as gpd
from folium import plugins

vin_df_slow_day1 = pd.read_csv('../visualization of vehicle telemetry/Packets_202306201310.csv')
# vin_df_slow_day1 = vin_df_slow_day1[vin_df_slow_day1['vin']=='MX1CEBCB0MK176800']
#
# vin_df_slow_day1['serverDateTime'] = pd.to_datetime(vin_df_slow_day1['serverDateTime'])
#
# vin_df_slow_day1 = vin_df_slow_day1[
#     (vin_df_slow_day1['serverDateTime'].dt.day == 11) & (vin_df_slow_day1['serverDateTime'].dt.month == 6)]

# coordinates_df = vin_df_slow_day1[vin_df_slow_day1['gpsDataReliability'] == True]
# coordinates_df = coordinates_df[['lon', 'lat', 'gpsSpeed']]
# coordinates_df.to_csv('Coordinates.csv', index=False)
# coordinates_df.drop_duplicates(keep='last')

all_points = vin_df_slow_day1[['lon', 'lat']]
all_lats = all_points['lat'].tolist()
all_lons = all_points['lon'].tolist()

coordinates_df = pd.read_csv('../visualization of vehicle telemetry/Coordinates.csv')
lats = coordinates_df['lat'].tolist()
lons = coordinates_df['lon'].tolist()

polylines = [(lats[i], lons[i]) for i in range(0, len(lats))]
colors = coordinates_df['gpsSpeed'].tolist()
m = folium.Map(location=[43.23, 76.9],
               zoom_start=13, prefer_canvas=True, disable_3d=False)
colormap = branca.colormap.LinearColormap(colors=['blue', 'green', 'yellow', 'red'], index=[10, 40, 60, 90], vmin=0,
                                          vmax=110)
colormap.caption = 'Vehicle speed'
colormap.add_to(m)

heat_data = [[round(all_lats[i], 6), round(all_lons[i], 6)] for i in range(0, len(all_points))]
plugins.HeatMap(heat_data, radius=15, name='Density of movement of vehicles').add_to(m)

Vehicle_track = folium.FeatureGroup(name='Vehicle track', show=False)
folium.ColorLine(positions=polylines,
                 name="Vehicle track",
                 colors=colors,
                 colormap=['b', 'g', 'y', 'r'],
                 nb_steps=20,
                 weight=5,
                 opacity=0.8).add_to(Vehicle_track)
track_points = folium.FeatureGroup(name='Track points', show=False)

icon = folium.features.CustomIcon('https://images-eu.ssl-images-amazon.com/images/I/517HQxbbFJL._UL1000_.jpg',
                                  icon_size=(20, 20))
folium.Marker([43.292935, 76.935238], icon=icon).add_to(Vehicle_track)
icon = folium.features.CustomIcon('https://images-eu.ssl-images-amazon.com/images/I/517HQxbbFJL._UL1000_.jpg',
                                  icon_size=(20, 20))
folium.Marker([43.280467, 76.910803], icon=icon).add_to(Vehicle_track)
icon = folium.features.CustomIcon('https://images-eu.ssl-images-amazon.com/images/I/517HQxbbFJL._UL1000_.jpg',
                                  icon_size=(20, 20))
folium.Marker([43.250794, 76.981398], icon=icon).add_to(Vehicle_track)

for i in range(0, len(lats)):
    folium.CircleMarker(location=[lats[i], lons[i]],
                        radius=3, popup=colors[i]).add_to(track_points)
track_points.add_to(m)
Vehicle_track.add_to(m)
folium.LayerControl().add_to(m)

m.save("index.html")
