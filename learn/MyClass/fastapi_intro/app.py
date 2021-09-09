from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/openapi.json")


@app.get("/")
async def root():
    return {"message": "Hello World"}

