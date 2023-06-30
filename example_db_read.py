import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    token = "hHSXQ4ARF4YYcQcDHaqZWZzjtGerYEmj0PK_yaV03yHcuiCP9o01MOdU2MrU36YUMrTcsOnG5QWIpfyF1AJ98g=="
    org = "ERENA"
    url = "http://localhost:8086"
    bucket = "db"

    # Create the InfluxDB client
    client = InfluxDBClient(url=url, token=token, org=org)

    # Create the query
    query = f'from(bucket:"{bucket}") |> range(start: -7d) |> filter(fn: (r) => r["_measurement"] == "measurement1")'

    # Execute the query
    result = client.query_api().query(query)

    # Process the results
    for table in result:
        for record in table.records:
            timestamp = record.get_time().isoformat()
            field1_value = record.values.get('tagname1')
            # Process or print the values as needed
            print(f"Timestamp: {timestamp}, Field1: {field1_value}")

    # Close the client
    client.close()


if __name__ == "__main__":
    main()
