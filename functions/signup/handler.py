import logging
import modules.sls_django
from http import HTTPStatus

from modules import cache
from modules import parameters
from modules import decorators

from database.identity.serializers import CreateIdentitySerializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@decorators.serialized_handler(
    input_serializer=CreateIdentitySerializer, output_serializer=None
)
def handler(event, context):
    return ({}, HTTPStatus.CREATED)
