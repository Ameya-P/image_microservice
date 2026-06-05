from db import connect_to_db
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from bson.objectid import ObjectId
import bson.errors
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

bucket = None

@asynccontextmanager
async def lifespan(app):
    # startup code
    global bucket
    bucket = connect_to_db()
    yield
    # shutdown code
    pass

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Define Routes Here ----
@app.post("/image/", response_class=PlainTextResponse)
async def upload_image(file: UploadFile = File(...)):
    file_bytes = await file.read()
    id = await bucket.upload_from_stream(file.filename, file_bytes)
    return str(id)

@app.get("/image/{id}")
async def get_image(id: str):
    try:
        object_id = ObjectId(id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=400, detail=f"Conversion failed. Invalid ID format: {id}")
    file = await bucket.open_download_stream(object_id)
    return StreamingResponse(file, media_type="image/jpeg")