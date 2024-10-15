from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.darwin.midtier.resources.account import router as ns1
from src.darwin.midtier.resources.assignment import router as ns2
from src.darwin.midtier.resources.course import router as ns3

# from midtier.resources.course import router as ns2
# from midtier.resources.grading import router as ns3

origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000", "http://172.20.129.207:3000"]

app = FastAPI()
app.include_router(ns1)
app.include_router(ns2)
app.include_router(ns3)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
