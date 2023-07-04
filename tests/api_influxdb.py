import requests

# Set up the API endpoint URL
url = "http://localhost:8086/query"

# Set up the myquery parameters
params = {
    "db": "db",
    "q": "SELECT * FROM sumo"
}

# Set up the headers with the API key
headers = {
    "Authorization": "I5Iyui0V6B-MLOX9Hm_GlcvC7ZqJVTMDF04fqfFsgDQjniavDldsZ4jhtfBOKKwi1l4ACjBarQXvDEFrYYZ6CQ=="
}

# Make the GET request with the headers
response = requests.get(url, params=params, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Process the response data
    data = response.json()
    # Access the results from the data object
    results = data["results"]
    # Access the first result
    first_result = results[0]
    # Access the series data (if available)
    series = first_result.get("series", [])
    # Access the data points (if available)
    if series:
        data_points = series[0].get("values", [])
        for point in data_points:
            # Process each data point
            print(point)
else:
    # Print the error message if the request failed
    print("Request failed with status code:", response.status_code)
