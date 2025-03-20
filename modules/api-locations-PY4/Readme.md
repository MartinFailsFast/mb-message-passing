SQL check: PGadmin
select * from location where person_id=5 and creation_time >='2019-07-05 15:00:00' and creation_time <='2025-07-07 15:00:00'


Apt Get:
    RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libpq-dev \
    build-essential \
    python3-dev \
    libffi-dev \
    bash \
    g++ \
    cmake \
    make \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*    


REST:
api-person-1     | DEBUG:root:Location: {'creation_time': '2020-08-15T10:37:06', 'latitude': '-122.290883', 'id': 30, 'person_id': 5, 'longitude': '37.55363'}


import requests

# Client class to fetch locations
class LocationClient:
    BASE_URL = "http://mb-cd0309-message-passing-projects-starter-api-locations-1:5001/api/locations"
    #http://{{host}}:{{port}}/api/persons

    def get_locations(self, person_id, start_date, end_date):
        """Fetch locations by person_id and time range."""
        params = {
            "person_id": person_id,
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            # Send the GET request
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Raise an error for non-2xx responses

            # Return raw JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
        except Exception as e:
            print(f"Error handling response: {e}")
            return []

# Example usage
if __name__ == "__main__":
    client = LocationClient()
    print("Fetching locations...")
    person_id = 5
    start_date = "2020-07-07T18:00:00"
    end_date = "2025-07-07T18:00:00"

    locations = client.get_locations(person_id, start_date, end_date)

    if locations:
        print("Retrieved locations:")
        for loc in locations:
            print(
                f"ID: {loc.get('id')}, Person ID: {loc.get('person_id')}, Lat: {loc.get('latitude')}, Long: {loc.get('longitude')}, Time: {loc.get('creation_time')}"
            )
    else:
        print("No locations found.")
