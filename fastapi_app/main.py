from fastapi import FastAPI
from crud import get_channels, get_products


app = FastAPI()

@app.get("/api/channels/type")
def channel_activity():
    result1 = get_channels()
    print("result " , result1)

    return result1

@app.get("/api/products/type")
def get_product():
    result2 = get_products()
    print("result " , result2)

    return result2
