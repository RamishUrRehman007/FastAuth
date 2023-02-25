import logging
from typing import Callable

import uvicorn  # type: ignore
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

import config
from error_handler import exception_handler
from exceptions import FastAuthAppError
from libs import log_sanitizer
from views import status_view, user_view


def init_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s",
        level=config.LOG_LEVEL,
    )
    log_sanitizer.sanitize_formatters(logging.root.handlers)


def include_routers(app: FastAPI) -> None:
    app.include_router(status_view.router, prefix="/v1")
    app.include_router(user_view.router, prefix="/v1")


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(FastAuthAppError, exception_handler)


def add_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def replace_content_type_header(
        request: Request, call_next: Callable
    ) -> Response:
        response = await call_next(request)
        if response.headers.get("content-type") == "application/json":
            response.headers["content-type"] = "application/json; charset=utf-8"
        return response

    @app.middleware("http")
    async def TokenMiddleware(request: Request, call_next):
        if request.url.path in routes_with_middleware:
            if "authorization" in request.headers.keys():
                logging.info("JWT Found")
                jwt_token = request.headers["authorization"].lstrip("Bearer").strip()
                auth_jwt = AuthJWT()
                csrf_protect = CsrfProtect()
                try:
                    jwt_data = auth_jwt.get_raw_jwt(jwt_token)
                    request.state.user_email = jwt_data["sub"]
                    csrf_protect.validate_csrf_in_cookies(request)
                except AuthJWTException:
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"detail": "Invalid JWT provided"},
                    )
                except CsrfProtectError as exc:
                    return JSONResponse(
                        status_code=exc.status_code, content={"detail": exc.message}
                    )
            else:
                logging.info("Middleware: Token does not exist")
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Token not supplied"},
                )

        return await call_next(request)


init_logging()

app = FastAPI(
    title="fast_auth",
    root_path=config.ROOT_PATH,
    openapi_url="/openapi.json" if config.ENVIRONMENT == "dev" else None,
)

include_routers(app)
add_exception_handlers(app)
add_middlewares(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
)


routes_with_middleware = ["/v1/auth/user"]


class JWTSettings(BaseModel):
    authjwt_secret_key: str = config.JWT_SECRET
    authjwt_access_token_expires: int = 60 * 60  # in seconds
    authjwt_encode_issuer: str = config.JWT_ISSUER


@AuthJWT.load_config
def get_jwt_config() -> JWTSettings:
    return JWTSettings()


class CsrfSettings(BaseModel):
    secret_key: str = config.CSRF_SECRET


@CsrfProtect.load_config
def get_csrf_config() -> CsrfSettings:
    return CsrfSettings()


@app.get("/")
async def root_view() -> RedirectResponse:
    return RedirectResponse(url=config.ROOT_PATH + "/docs", status_code=303)


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        log_level=config.UVICORN_LOG_LEVEL,
        reload=config.ENABLE_RELOAD_UVICORN,
    )
