import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.locationclient import LocationClient
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect-api")


class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """

        '''
                # Initialize the client
        location_client = LocationClient()

        # Replace the DB query with REST API call
        locations_data = location_client.get_locations(
            person_id=person_id,
            start_date=start_date.strftime("%Y-%m-%dT%H:%M:%S"),
            end_date=end_date.strftime("%Y-%m-%dT%H:%M:%S")
        )
        locations = []
        # Loop through each location in the API response
        for loc_data in locations_data:
            location = Location(
                id=loc_data['id'],
                person_id=loc_data['person_id'],
                longitude=loc_data['longitude'],
                latitude=loc_data['latitude'],
                creation_time=loc_data['creation_time']
            )
            locations.append(location)


        # Check if locations returned successfully
        if not loc_data:
            logging.debug("No locations found or API call failed.")

        '''
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()
        

        # Cache all users in memory for quick lookup
        person_map: Dict[str, Person] = {person.id: person for person in PersonService.retrieve_all()}

        # Prepare arguments for queries
        data = []
        for location in locations:
            logging.debug(f"Location: {location.longitude}, {location.latitude}")
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        result: List[Connection] = []
        for line in tuple(data):
            for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
            ) in db.engine.execute(query, **line):
                location = Location(
                    id=location_id,
                    person_id=exposed_person_id,
                    creation_time=exposed_time,
                )
                location.set_wkt_with_coords(exposed_lat, exposed_long)

                result.append(
                    Connection(
                        person=person_map[exposed_person_id], location=location,
                    )
                )

        return result



class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        logging.debug(f"Person found: id={person.id}, first_name={person.first_name}, last_name={person.last_name}, company_name={person.company_name}")
        return person
    
    @staticmethod
    def retrieveNew(person_id: int) -> Person:
        person = db.session.query(Person).filter_by(id=int(person_id)).first()
        logging.debug(f"Person found: id={person.id}, first_name={person.first_name}, last_name={person.last_name}, company_name={person.company_name}")
        if not person:
            logging.debug(f"Person not found")
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
