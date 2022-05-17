import logging
import modules.sls_django

from http import HTTPStatus


from modules.decorators import action_method, generic_request_handler
from modules.actions import Actions

from database.pets.models import Pet
from database.identity.models import Identity

from database.pets.serializers import (
    PetSerializer,
    ListPetSerializer
)
from logic import pets

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@action_method(output_serializer=ListPetSerializer, protected=True)
def list_pets(event, context=None):
    response = pets.list_pets()
    return response, HTTPStatus.OK


@generic_request_handler(
    methods=[list_pets]
)
def handler(event, context, response):
    return response

# class PetPermissions:
#     protected = [
#         Actions.ActionUpdate,
#         Actions.ActionGeneric,
#         Actions.ActionCreate,
#     ]


# @serialized_handler(
#     input_serializer=PetSerializer,
#     output_serializer=PetSerializer,
#     permission_class=PetPermissions,
#     allowed_actions=[
#         Actions.ActionUpdate,
#         Actions.ActionCreate,
#         Actions.ActionRetrieve,
#         Actions.ActionDelete,
#         Actions.ActionList,
#     ],
#     action_serializers={
#         Actions.ActionUpdate: PetSerializer,
#         Actions.ActionCreate: PetSerializer,
#         Actions.ActionList: ListPetSerializer,
#         Actions.ActionRetrieve: ListPetSerializer,
#     },
# )
# def handler(event, context):

#     action = event.get("action")

#     response = None
#     status = None

#     if action == Actions.ActionRetrieve:
#         response = pets.get_pet(pet_id=event["pet_id"])
#         status = HTTPStatus.OK

#     elif action == Actions.ActionUpdate:
#         response = pets.update_pet(
#             pet_id=event.get("pet_id"),
#             name=event.get("name")

#         )
#         status = HTTPStatus.OK

#     elif action == Actions.ActionCreate:
#         response = pets.create_pet(
#             name=event.get("name"),
#         )

#         status = HTTPStatus.CREATED

#     elif action == Actions.ActionDelete:
#         response = pets.delete_pet(pet_id=event["pet_id"])
#         status = HTTPStatus.NO_CONTENT

#     elif action == Actions.ActionList:
#         response = pets.list_pets()
#         status = HTTPStatus.OK

#     return (response, status)
