from sanic import Sanic
from sanic.response import text
import psycopg2

app = Sanic("app")

@app.route('/getcarcoord/<vin:str>')
async def test(request, vin: str):
    try:
        conn = psycopg2.connect("dbname='vehicle_telemetry' user='postgres' host='localhost' password='1111'")
        with conn:
            with conn.cursor() as db_curs:
                db_curs.execute(f" SELECT lon, lat, \"gpsSpeed\" FROM public.vehicle_data WHERE vin = '{vin}'; ")
                result = db_curs.fetchall()
                return text(result)

    except Exception as inst:
        print(inst)
        return text("Error")


if __name__ == '__main__':
    app.run()
