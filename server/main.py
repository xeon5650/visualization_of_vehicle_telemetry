from sanic import Sanic, response, json as sjs
import psycopg2
import json
from sanic_ext import Extend

app = Sanic("app")
app.config.CORS_ORIGINS = "*"
Extend(app)

@app.route('/getcarcoordlocaly/<vin:str>/<lat:float>/<lon:float>')
async def getcarcoord(request, vin: str, lat: float, lon: float):
    try:
        conn = psycopg2.connect("dbname='vehicle_telemetry' user='postgres' host='localhost' password='1111'")
        with conn:
            with conn.cursor() as db_curs:
                db_curs.execute(f" SELECT lon, lat, \"gpsSpeed\" FROM public.vehicle_data WHERE vin = '{vin}' AND lon-{lon} < 3 AND lat-{lat}<3; ")
                result = db_curs.fetchall()

                heatdata = []
                for el in result:
                    heatdata.append([el[1], el[0], el[2]])

                answer = json.dumps(heatdata)

                print("Here")

                return sjs(answer, headers={"Access-Control-Allow-Methods":"*", "Access-Control-Allow-Headers":"Content-type", "Access-Control-Allow-Origin":"http://localhost:63342/vehicle_telemetry/index.html?_ijt=c0sm6iss7bp6ht0cmieim292uf&_ij_reload=RELOAD_ON_SAVE"})


    except Exception as inst:
        print(inst)
        return json({"Error": inst})


if __name__ == '__main__':
    app.run()
