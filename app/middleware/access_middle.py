#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from http import HTTPStatus

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.log import log


class AccessMiddleware(BaseHTTPMiddleware):
    """
    记录请求日志
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # log request
        client_addr = (
            f"{request.client.host}:{request.client.port}"
            if request.client
            else "unknown"
        )
        http_version = (
            request.scope.get("type", "").upper()
            + "/"
            + request.scope.get("http_version", "")
        )
        req_method = request.method
        req_path = request.scope.get("path", "")
        if request.query_params:
            req_path += "?" + str(request.query_params)
        trace_id = request.headers.get("x-apm-traceid")
        log.bind(client_addr=client_addr, trace_id=trace_id).info(
            f'request: "{req_method} {req_path} {http_version}"'
        )

        # call function
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        total_time = f"{(end_time - start_time) * 1000:.0f}ms"

        # 取消以下注释可以把response body打印出来
        # response_body = [section async for section in response.body_iterator]
        # response.body_iterator = iterate_in_threadpool(iter(response_body))
        # log.info(f"response_body={response_body[0].decode()}")

        # log response
        status_code = response.status_code
        try:
            status_phrase = HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""
        status_and_phrase = f"{status_code} {status_phrase}"
        log.bind(client_addr=client_addr, trace_id=trace_id).info(
            f'response: "{request.method} {req_path} {http_version}" {status_and_phrase} - {total_time}'
        )

        return response
