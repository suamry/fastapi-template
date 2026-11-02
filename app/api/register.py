#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_oauth2_redirect_html,
    get_swagger_ui_html,
    get_redoc_html,
)

from app.api.routers import root_router
from app.api.routers import v1_router
from app.common.exception.exception_handler import register_exception
from app.config.conf import settings
from app.config.path_conf import STATIC_PATH
from app.middleware import register_middleware


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
    )

    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 全局异常处理
    register_exception(app)

    # 注册静态文件
    register_static_file(app)

    # 代理 swagger ui 静态资源
    register_swagger(app)

    return app


def register_router(app: FastAPI):
    """
    路由

    :param app: FastAPI
    :return:
    """
    app.include_router(root_router)
    app.include_router(v1_router)


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务

    :param app:
    :return:
    """
    import os
    from fastapi.staticfiles import StaticFiles

    if not os.path.exists(STATIC_PATH):
        os.mkdir(STATIC_PATH)
    app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")


def register_swagger(app: FastAPI):
    @app.get(settings.SWAGGER_UI_OAUTH2_REDIRECT_URL, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=settings.OPENAPI_URL,
            title=settings.TITLE + " - Swagger UI",
            swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui/swagger-ui.css",
            swagger_favicon_url="/static/swagger-ui/favicon.png",
        )

    @app.get(settings.REDOCS_URL, include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=settings.OPENAPI_URL,
            title=settings.TITLE + " - ReDoc",
            redoc_js_url="/static/swagger-ui/redoc.standalone.js",
            redoc_favicon_url="/static/swagger-ui/favicon.png",
        )
