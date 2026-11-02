import json
from typing import Optional

from pydantic import BaseModel, Field


class HelloReq(BaseModel):
    name: str = Field(title="姓名", description="用户姓名", examples=["张三"])
    age: Optional[int] = Field(
        default=None, title="年龄", description="用户年龄", examples=[18], ge=0, le=150
    )
    address: Optional[str] = Field(
        default=None, title="地址", description="用户地址", examples=["中国"]
    )


class HelloResp(HelloReq):
    pass


if __name__ == "__main__":
    # dict to pydantic model
    data = {"name": "李四"}
    model = HelloReq.parse_obj(data)
    print(repr(model))
    # HelloReq(name='李四', age=None, address=None)

    # 导出 OpenAPI schema
    print(json.dumps(HelloReq.model_json_schema()))
    # {"properties":{"name":{"description":"用户姓名","example":"张三","title":"姓名","type":"string"},"age":{"anyOf":[{"maximum":150,"minimum":0,"type":"integer"},{"type":"null"}],"default":null,"description":"用户年龄","example":18,"title":"年龄"},"address":{"anyOf":[{"type":"string"},{"type":"null"}],"default":null,"description":"用户地址","example":"中国","title":"地址"}},"required":["name"],"title":"HelloReq","type":"object"}
