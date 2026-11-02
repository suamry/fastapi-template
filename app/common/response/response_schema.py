#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, Dict, Generic, Optional, Set, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

# Define a TypeVar for generic ResponseModel
T = TypeVar("T")

# Define custom encoder type
_CustomJsonEncoder = Union[Set[Union[int, str]], Dict[Union[int, str], Any]]

__all__ = ["ResponseModel", "ResponseBase", "encode_json"]


def encode_json(data: Any) -> Any:
    """
    Encodes data to JSON-compatible format using FastAPI's jsonable_encoder.
    Custom encoder for datetime objects is applied.

    :param data: The data to encode.
    :return: JSON-compatible data.
    """
    return jsonable_encoder(
        data,
        custom_encoder={datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")},
    )


class ResponseModel(BaseModel, Generic[T]):
    """
    Generic unified response model for FastAPI endpoints.

    :param T: The type of the data payload.
    """

    code: int = Field(200, description="Status code")
    message: str = Field("Success", description="Response message")
    data: Optional[T] = Field(None, description="Response data")

    class Config:
        json_encoders = {datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")}
        arbitrary_types_allowed = True


class ResponseBase(Generic[T]):
    @staticmethod
    def _construct_response(
        *,
        code: int,
        message: str,
        data: Optional[T] = None,
        exclude: Optional[_CustomJsonEncoder] = None,
    ) -> ResponseModel[T]:
        """
        Constructs the response dictionary.

        :param code: Status code.
        :param message: Response message.
        :param data: Response data.
        :param exclude: Fields to exclude from data.
        :return: ResponseModel instance.
        """
        encoded_data = encode_json(data) if data is not None else None
        return ResponseModel[T](code=code, message=message, data=encoded_data)

    @staticmethod
    def success(
        *,
        message: str = "Success",
        data: Optional[T] = None,
        exclude: Optional[_CustomJsonEncoder] = None,
    ) -> ResponseModel[T]:
        """
        Returns a success response.

        :param message: Success message.
        :param data: Response data.
        :param exclude: Fields to exclude from data.
        :return: Success response model.
        """
        return ResponseBase._construct_response(
            code=200, message=message, data=data, exclude=exclude
        )

    @staticmethod
    def fail(
        *,
        code: int = 400,
        message: str = "Bad Request",
        data: Optional[T] = None,
        exclude: Optional[_CustomJsonEncoder] = None,
    ) -> ResponseModel[T]:
        """
        Returns a failure response.

        :param code: Error status code.
        :param message: Error message.
        :param data: Error data.
        :param exclude: Fields to exclude from data.
        :return: Failure response model.
        """
        return ResponseBase._construct_response(
            code=code, message=message, data=data, exclude=exclude
        )

    @staticmethod
    def response_200(
        *,
        message: str = "Success",
        data: Optional[T] = None,
        exclude: Optional[_CustomJsonEncoder] = None,
    ) -> ResponseModel[T]:
        """
        Returns a 200 OK response.

        :param message: Success message.
        :param data: Response data.
        :param exclude: Fields to exclude from data.
        :return: 200 OK response model.
        """
        return ResponseBase._construct_response(
            code=200, message=message, data=data, exclude=exclude
        )


# 使用泛型实例化 ResponseBase
response_base: ResponseBase[Any] = ResponseBase()
