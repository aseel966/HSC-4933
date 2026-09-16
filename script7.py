import requests

# Census API information
YEAR = 2023
DATASET = "acs/acs5"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "4fd3ba416db903a3b38441fb781e516d1023a624"

# Ask user for state FIPS codes
print("Census Population Lookup")
print("------------------------")
print("Example: 06 = California, 12 = Florida, 36 = New York")
state_code = input("Enter The State FIPS Code:").strip()

# Ask user for variable name
variable = input("Enter the variable names that you would like data for:").strip()

# Build API request
params = {
    "get": f"NAME,{variable}",
    "for": f"state:{state_code}",
    "key": API_KEY,
}

# Send request
response = requests.get(URL, params=params)

print(response.url)
print(response)

# Process response
if response.status_code != 200:
    print(f"Request failed ({response.status_code})")
    print(response.text)
    raise SystemExit

data=response.json()

print(f"Got {len(data) -1} rows back.")

for i in data:
    print(i)