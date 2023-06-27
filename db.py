import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    token = "t_D61HyyeQ1899wEL-ehKWtSvRwxjKDFzIgPUVr9YTP61HO866jtj8Wlejx-0ZmuUIs_upaYBTfi8sXJkq_XHA=="
    org = "ERENA"
    url = "http://localhost:8086"
    bucket = "db"

    write_client = InfluxDBClient(url=url, token=token, org=org)
    write_api = write_client.write_api(write_options=SYNCHRONOUS)

    id_counter = 1  # Initialize the ID counter

    for value in range(5):
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", value)
            .field("id", id_counter)  # Add the ID field to the point
        )
        write_api.write(bucket=bucket, org=org, record=point)
        id_counter += 1  # Increment the ID counter
        time.sleep(1)  # Separate points by 1 second


if __name__ == "__main__":
    main()
