from app.schemas.greet_schema import HelloReq, HelloResp


def post_hello(dto: HelloReq):
    # TODO：业务逻辑
    return HelloResp.model_validate(dto.model_dump())
