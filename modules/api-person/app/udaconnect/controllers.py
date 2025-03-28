from datetime import datetime

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, fields
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

# Define API model directly from the DB model fields
person_model = api.model(
    "Person",
    {
        "id": fields.Integer(readOnly=True, description="Person ID"),
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "company_name": fields.String(required=True, description="Company name"),
    },
)



# TODO: This needs better exception handling

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    @api.expect(person_model)  # Ensure Swagger UI expects the model
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person

