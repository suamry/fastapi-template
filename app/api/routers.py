#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.api.v1.common.common import common
from app.api.v1.greet.hello import greet_router

# 根路由
root_router = APIRouter()
root_router.include_router(common, tags=['通用'])

# v1路由
v1_router = APIRouter(prefix='/v1')
v1_router.include_router(greet_router, prefix='/greet', tags=['greet group'])
