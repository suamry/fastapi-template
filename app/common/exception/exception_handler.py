from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from starlette.responses import JSONResponse
from uvicorn.protocols.http.h11_impl import STATUS_PHRASES

from app.common.exception.errors import BaseExceptionMixin
from app.common.response.response_schema import response_base
from app.config.conf import settings


def _get_exception_code(status_code):
    """
    获取返回状态码, OpenAPI, Uvicorn... 可用状态码基于 RFC 定义, 详细代码见下方链接

    `python 状态码标准支持 <https://github.com/python/cpython/blob/6e3cc72afeaee2532b4327776501eb8234ac787b/Lib/http
    /__init__.py#L7>`__

    `IANA 状态码注册表 <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`__

    :param status_code:
    :return:
    """
    try:
        STATUS_PHRASES[status_code]
    except Exception:
        code = 400
    else:
        code = status_code
    return code


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):  # noqa
        """
        全局HTTP异常处理

        :param request:
        :param exc:
        :return:
        """
        response = response_base.fail(
            code=exc.status_code, message=f"[{exc.__class__.__name__}] {exc.detail}"
        )
        return JSONResponse(
            status_code=_get_exception_code(exc.status_code),
            content=response.model_dump(),
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    def all_exception_handler(request: Request, exc):
        """
        全局异常处理

        :param request:
        :param exc:
        :return:
        """
        # 常规
        if isinstance(exc, ValidationError):
            message = ""
            for error in exc.errors():
                field = error["loc"][-1]
                _msg = error["msg"]
                message += f"{field} {_msg},"
            return JSONResponse(
                status_code=422,
                content={
                    "detail": f"[ValidationError] {'请求参数非法' if len(message) == 0 else f'请求参数非法: {message[:-1]}'}",
                    "errors": exc.errors() if message == "" else None,
                },
            )

        # 自定义
        if isinstance(exc, BaseExceptionMixin):
            response = response_base.fail(
                code=exc.code,
                message=f"[{exc.__class__.__name__}] {str(exc.message)}",
                data=exc.data if exc.data else None,
            )
            return JSONResponse(
                status_code=_get_exception_code(exc.code),
                content=response.model_dump(),
            )
        else:
            error_message = (
                str(exc) if settings.UVICORN_RELOAD else "Internal Server Error"
            )
            response = response_base.fail(
                code=500,
                message=f"[{exc.__class__.__name__}] {error_message}",
            )
            return JSONResponse(
                status_code=500,
                content=response.model_dump(),
            )
