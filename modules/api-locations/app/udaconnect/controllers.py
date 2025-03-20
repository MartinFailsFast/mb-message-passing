from datetime import datetime
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
import logging


DATE_FORMAT = "%Y-%m-%d"
#DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# Get the logger for this specific class/module
# logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("udaconnect")

# TODO: This needs better exception handling

@api.route("/locations")
@api.route("/locations/<int:location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):

    # Retrieve all locations or a specific location
    @responds(schema=LocationSchema(many=True))
    def get(self, location_id=None) -> List[Location]:
        try:
            # Check for the query parameters person_id, start_date, end_date
            logging.debug(f"Get Location : {request}")
            person_id = request.args.get('person_id')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            if location_id:
                location = LocationService.retrieve(location_id)
                return [location] if location else []

            if person_id and start_date and end_date:
                try:
                    start_date = datetime.strptime(start_date, DATE_FORMAT)
                    end_date = datetime.strptime(end_date, DATE_FORMAT)
                except ValueError as e:
                    return {"error": f"Invalid date format: {str(e)}"}, 400

                locations = LocationService.retrieve_user_locations(
                    person_id=int(person_id),
                    start_time=start_date,
                    end_time=end_date
                )
                return locations

            locations = LocationService.retrieve_all()
            return locations

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return {"error": "An unexpected error occurred. Please try again later."}, 500


    # Create a new location
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        location_data = request.get_json()
        logging.debug(f"Received data: {location_data}")
        location: Location = LocationService.create(location_data)
        return location
        #return jsonify(location_data), 201


@api.route("/locations/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema(many=True))  # Fixed here
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)
        print(f"Distance: {start_date} , {end_date}, {distance}" )

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results  
