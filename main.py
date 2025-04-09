from fastapi import FastAPI
from dockerflow.fastapi import router as dockerflow_router

app = FastAPI()
app.include_router(dockerflow_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
