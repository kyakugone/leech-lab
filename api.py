import os
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"


app = FastAPI(default_response_class=UTF8JSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("leeches.sql") as f:
    LEECH_QUERY = f.read()


def get_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"), row_factory=dict_row)


@app.get("/leeches")
def leeches():
    with get_connection() as conn:
        return conn.execute(LEECH_QUERY).fetchall()


@app.get("/passages")
def passages():
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, created_at, words, data FROM passages ORDER BY created_at DESC"
        ).fetchall()

@app.get("/passages/{passage_id}")
def passage(passage_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, created_at, words, data FROM passages WHERE id = %s",
            (passage_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Passage not found")
        return row