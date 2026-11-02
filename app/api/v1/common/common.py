#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.common.response.response_schema import response_base

common = APIRouter()


@common.get('/healthcheck', summary='健康检查')
async def healthcheck():
    return response_base.success(message='OK')
