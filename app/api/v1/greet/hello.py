#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.common.exception.errors import ServerError
from app.common.response.response_schema import ResponseModel, response_base
from app.schemas.greet_schema import HelloReq, HelloResp
from app.services.greet import hello_service

greet_router = APIRouter()


@greet_router.get("/hello", summary="hello")
async def say_hello():
    return response_base.success(message="OK")


@greet_router.post("/hello", summary="hello(return_type_annotation)")
async def post_hello(dto: HelloReq) -> ResponseModel[HelloResp]:
    # TODO: 调用业务逻辑
    data = hello_service.post_hello(dto)
    return response_base.success(data=data)


# 注意: response_model 参数和返回类型注解(->)在FastAPI中等价
# 两者都可以用于定义API响应的数据模型，但推荐使用返回类型注解
# 因为:
# 1. 更符合Python类型提示规范
# 2. IDE能提供更好的类型检查和自动补全
# 3. 代码可读性更高
@greet_router.post(
    "/hello_response_model",
    summary="hello(response_model)",
    response_model=ResponseModel[HelloResp],
)
async def post_hello_2(dto: HelloReq):
    # TODO: 调用业务逻辑
    data = hello_service.post_hello(dto)
    return response_base.success(data=data)


@greet_router.post("/raiseError", summary="raise error")
async def raise_error():
    raise ServerError(message="测试抛出500错误")
