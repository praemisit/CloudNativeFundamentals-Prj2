from datetime import datetime

from app.udaconnect.models import Person
from app.udaconnect.schemas import (
    PersonSchema,
)
from app.udaconnect.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect Person Service", description="Participating Persons.")  # noqa

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>", methods=['GET', 'DELETE'])
@api.param("person_id", "Unique ID for a given Person", _in="query")
@api.doc(responses={400: 'Person ID not found', 200: 'OK'})
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person

    def delete(self, person_id) -> Person:
        status = PersonService.delete(person_id)
        if status is person_id:
            return [{'person_id': person_id, 'message': 'Deleted successfully'}], 200
        elif status is None:
            return [{'person_id': person_id, 'message': 'Person was not found'}], 400