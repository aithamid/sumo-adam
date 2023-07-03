import sys
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    with InfluxDBClient.from_config_file("creds.toml") as client:
        result = client.query_api().query("""
                    from(bucket: "db")
                |> range(start: -1d)
                |> filter(fn: (r) => r["_measurement"] == "sumo")
                |> filter(fn: (r) => r["_field"] == "co2" or r["_field"] == "latitude" or r["_field"] == "longitude" or r["_field"] == "speed" )
                |> last()
                |> pivot(rowKey:["_time"], columnKey:["_field"], valueColumn:"_value")
                """)
        print(result.to_json())


if __name__ == "__main__":
    sys.exit(main())
