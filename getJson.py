import requests

# Make a GET request to the URL
response = requests.get('http://localhost:5000/')

# Print the response status code
print(response.status_code)

# Print the response content
print(response.content)