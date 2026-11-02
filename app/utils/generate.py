#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import uuid


def get_uuid() -> str:
    """
    生成uuid

    :return: str(uuid)
    """
    return str(uuid.uuid4())


def get_uuid_hex() -> str:
    """
    生成无横杆uuid

    :return:
    """
    return uuid.uuid4().hex


def get_current_timestamp() -> float:
    """
    生成当前时间戳

    :return:
    """
    return datetime.datetime.now().timestamp()


if __name__ == '__main__':
    print(get_uuid_hex())
