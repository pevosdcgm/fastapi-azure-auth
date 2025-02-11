from typing import Dict, Union
import logging

from demo_project.api.dependencies import multi_auth, multi_auth_b2c
from demo_project.schemas.hello_world import TokenType
from fastapi import APIRouter, Depends, Request

from fastapi_azure_auth.user import User

log = logging.getLogger("__main__." + __name__)
log.propagate=True
log.info("hello_world_multi_auth info")
log.warning("hello_world_multi_auth warning ")
log.exception("hello_world_multi_auth exception")

router = APIRouter()


@router.get(
    '/hello-multi-auth',
    response_model=TokenType,
    summary='Say hello with openid',
    name='hello_world_multi_auth',
    operation_id='helloWorldMultiAuth',
)
async def world(request: Request, auth: Union[str, User] = Depends(multi_auth)) -> Dict[str, bool]:
    """
    Wonder how this auth is done?
    """
    if isinstance(auth, str):
        # An API key was used
        return {'api_key': True, 'azure_auth': False}
    return {'api_key': False, 'azure_auth': True}


@router.get(
    '/hello-multi-auth-b2c',
    response_model=TokenType,
    summary='Say hello with an API key',
    name='hello_world_api_key',
    operation_id='helloWorldApiKey',
)
async def world_b2c(request: Request, auth: Union[str, User] = Depends(multi_auth_b2c)) -> Dict[str, bool]:
    """
    Wonder how this auth is done?
    """
    if isinstance(auth, str):
        # An API key was used
        return {'api_key': True, 'azure_auth': False}
    return {'api_key': False, 'azure_auth': True}
