import requests
# Set the API endpoint URL
api_url = "http://example.com/api/endpoint"
# Set the API key as a query parameter
api_key = "your_api_key"
query_params = { "api_key": api_key }
# Make the request to the API
response = requests.get(api_url, params=query_params)
# Print the response status code
print(response.status_code)
# Print the response content
print(response.content)










 








