import requests

# URL of your Flask application's POST endpoint
url = 'http://localhost:5000/cars/carX'

# Data for the POST request
data = {
    'vehicle': 'Toyota',
    'model': 'Camry',
    'year': 2022
}

# Send the POST request
response = requests.post(url)

# Check the response status code
if response.status_code == 200:
    print('Car added successfully.')
else:
    print('Failed to add car.')

# Print the response content
print(response.content)
