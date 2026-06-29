from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(message: str = "success", data=None):

    content = {
        "code":200,
        "message":message,
        "data":data
    }
    # 把任何的fastapi、pydantic、orm对象都要正常响应 -> code，message、data
    return JSONResponse(content=jsonable_encoder(content))
