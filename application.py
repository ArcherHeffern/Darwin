from fastapi import FastAPI
from src.darwin.midtier.resources.account import router as ns1
from src.darwin.midtier.resources.assignment import router as ns2
from src.darwin.midtier.resources.course import router as ns3
# from midtier.resources.course import router as ns2
# from midtier.resources.grading import router as ns3


app = FastAPI()
app.include_router(ns1)
app.include_router(ns2)
app.include_router(ns3)