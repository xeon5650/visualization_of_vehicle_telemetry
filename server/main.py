from sanic import Sanic
from sanic.response import html, text
import psycopg2
import folium
from folium import plugins
import branca

app = Sanic("app")

@app.route('/getcarcoord/<vin:str>')
async def test(request, vin: str):
    try:
        conn = psycopg2.connect("dbname='vehicle_telemetry' user='postgres' host='localhost' password='1111'")
        with conn:
            with conn.cursor() as db_curs:
                db_curs.execute(f" SELECT lon, lat, \"gpsSpeed\" FROM public.vehicle_data WHERE vin = '{vin}'; ")
                result = db_curs.fetchall()

                world_map = folium.Map(location=[43.23, 76.9], zoom_start=13, prefer_canvas=True, disable_3d=False)

                colormap = branca.colormap.LinearColormap(colors=['blue', 'green', 'yellow', 'red'],
                                                          index=[10, 40, 60, 90], vmin=0,
                                                          vmax=110)
                colormap.caption = 'Vehicle speed'
                colormap.add_to(world_map)

                heatdata = []
                for el in result:
                    heatdata.append([el[1], el[0], el[2]])

                plugins.HeatMap(heatdata, radius=18).add_to(world_map)

                return html(world_map)


    except Exception as inst:
        print(inst)
        return text("Error")


if __name__ == '__main__':
    app.run()
