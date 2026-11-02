#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ 配置类 """
    # FastAPI
    TITLE: str = 'FastAPI APP'
    VERSION: str = 'v0.1'
    DESCRIPTION: str = """
[redocs](/v1/redocs)
    """
    DOCS_URL: str = '/v1/docs'
    REDOCS_URL: str = '/v1/redocs'
    OPENAPI_URL: str = '/v1/openapi'
    SWAGGER_UI_OAUTH2_REDIRECT_URL: str = '/docs/oauth2-redirect'

    # Uvicorn
    UVICORN_HOST: str = '0.0.0.0'
    UVICORN_PORT: int = 8899
    UVICORN_RELOAD: bool = True
    # 如果此处为True，在 @app.on_event("startup") 时发生异常，则程序不会终止，详情：https://github.com/encode/starlette/issues/486
    UVICORN_WORKERS: int = 1

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = True


@lru_cache()
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()
