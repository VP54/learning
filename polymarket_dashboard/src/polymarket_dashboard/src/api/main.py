from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/run_workflow/{workflow_id}")
def run_workflow(workflow_id: int | str):
    return {
        "workflow_id": workflow_id
    }
