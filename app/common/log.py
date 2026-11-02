#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from loguru import logger

from app.config import path_conf
from app.utils.singleton import SingletonMeta

log_format = (
    "[ <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <level>{level}</level>]"
    "[ <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> ] "
    "<level>{extra[client_addr]}{message}</level>"
)


class Logger(metaclass=SingletonMeta):
    @staticmethod
    def patch(record):
        # 额外信息后补空格
        extra = record["extra"]

        # client地址
        if extra["client_addr"]:
            extra["client_addr"] = f"from: {extra['client_addr']}"

            # 鲸云trace_id记录
            if extra["trace_id"]:
                extra["client_addr"] += f"({extra['trace_id']})"

            extra["client_addr"] += " - "

        return record

    @staticmethod
    def init():
        logger.configure(
            extra={"client_addr": "", "trace_id": ""},
            patcher=lambda record: Logger.patch(record),
        )
        logger.remove()
        logger.add(sys.stderr, format=log_format)

    @staticmethod
    def log():
        Logger.init()
        if not os.path.exists(path_conf.LOG_PATH):
            os.mkdir(path_conf.LOG_PATH)

        # 日志文件
        log_file = os.path.join(path_conf.LOG_PATH, "FastAPI.log")

        # loguru日志
        # more: https://github.com/Delgan/loguru#ready-to-use-out-of-the-box-without-boilerplate
        logger.add(
            log_file,
            encoding="utf-8",
            level="DEBUG",
            rotation="00:00",  # 每天 0 点创建一个新日志文件
            retention="30 days",  # 定时自动清理文件
            enqueue=True,  # 异步安全
            backtrace=True,  # 错误跟踪
            diagnose=True,
            format=log_format,
        )

        return logger


log = Logger().log()
