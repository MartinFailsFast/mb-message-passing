import requests
import os

# Client class to fetch locations
class PersonClient:
    BASE_URL = os.environ["PERSON_HOST"]
     #= "http://mb-cd0309-message-passing-projects-starter-api-person-1:5000/api/persons"
    #BASE_URL = "http://localhost:5000/api/persons"



    def get_persons(self):
        """Fetch persons"""
        params = {}
        

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
    client = PersonClient()
    print("Fetching Persons...")
    persons = client.get_persons()

    if persons:
        print("Retrieved Persons:")
        for per in persons:
            print(
                f"ID: {per.get('id')}, {per.get('first_name')},{per.get('last_name')},{per.get('company_name')}"
            )
    else:
        print("No Persons found.")

