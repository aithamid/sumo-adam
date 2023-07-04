import sys
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS


def getLastAll():
    with InfluxDBClient.from_config_file("creds.toml") as client:
        result = client.query_api().query("""
                    from(bucket: "db")
                          |> range(start: -1d)
                          |> filter(fn: (r) => r["_measurement"] == "sumo")
                          |> filter(fn: (r) => r["_field"] == "co2" or r["_field"] == "latitude" or r["_field"] == "longitude" or r["_field"] == "speed" or  r["_field"] == "simu_id")
                          |> group(columns: ["_field",  "vehicle_id"])
                          |> last()
                          |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
                          |> yield(name: "last_result")
                """)
        myjson = result.to_json()
        return myjson


def getLastSimuId():
    myjson = getLastAll()
    data = json.loads(myjson)
    if not data or len(data) == 0:
        return 0
    else:
        simu_ids = [record['simu_id'] for record in data]
        return int(simu_ids[0])


def main():
    myjson = getLastAll()
    print(myjson)
    simu_id = getLastSimuId()
    print("Simu ID:", simu_id)


if __name__ == "__main__":
    sys.exit(main())
