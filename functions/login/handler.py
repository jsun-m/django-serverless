import logging
import modules.sls_django

from http import HTTPStatus
from modules import decorators

from database.identity.serializers import LoginSerializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@decorators.serialized_handler(
    input_serializer=LoginSerializer, output_serializer=None,
)
def handler(event, context):
    token = event.get("token")
    body = {"token": token["key"]}
    return (body, HTTPStatus.OK)
