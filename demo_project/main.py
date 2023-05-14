import logging
from argparse import ArgumentParser

import uvicorn
from demo_project.api.api_v1.api import api_router_azure_auth, api_router_graph, api_router_multi_auth
from demo_project.api.dependencies import azure_scheme
from demo_project.core.config import settings
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

#log = logging.getLogger(__name__)

app = FastAPI(
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': settings.OPENAPI_CLIENT_ID,
        'additionalQueryStringParams': {'prompt': 'consent'},
    },
    version='1.0.0',
    description='## Welcome to my API! \n This is my description, written in `markdown`',
    title=settings.PROJECT_NAME,
)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:  # pragma: no cover
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()


app.include_router(
    api_router_azure_auth,
    prefix=settings.API_V1_STR,
    dependencies=[Security(azure_scheme, scopes=['user_impersonation'])],
)
app.include_router(
    api_router_multi_auth,
    prefix=settings.API_V1_STR,
    # Dependencies specified on the API itself
)
app.include_router(
    api_router_graph,
    prefix=settings.API_V1_STR,
    # Dependencies specified on the API itself
)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--api', action='store_true')
    parser.add_argument('--reload', action='store_true')

    parser.add_argument( '-log',
                     '--loglevel',
                     default='warning',
                     help='Provide logging level. Example --loglevel debug, default=warning' )

    args = parser.parse_args()
    
    logging.basicConfig( level=args.loglevel.upper(), format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#log = logging.getLogger(__name__)

    logging.info( 'Logging now setup.' )
    log = logging.getLogger(__name__)
    log.info("info")
    log.warning("warning")

    if args.api:
#        uvicorn.run('main:app', reload=args.reload)
        uvicorn.run('main:app', host='localhost', port=8010, reload=args.reload)
    else:
        raise ValueError('No valid combination of arguments provided.')
