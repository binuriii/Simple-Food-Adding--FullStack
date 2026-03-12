import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Fruit(BaseModel):
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]

app = FastAPI(debug=True) # create fast api application

origins = [
    "http://localhost:5173"
] # create list of origins that are allowed, inside of the list define endpoint / URL of the frontend server

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # we can send things like JWT tokens
    allow_methods=["*"], # if you want to block delete or put method
    allow_headers=["*"], 
)

memory_db = {"fruits": []} # database that will not persist when application shutdown

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory_db["fruits"])

@app.post("/fruits")
def add_fruit(fruit: Fruit):
    memory_db["fruits"].append(fruit)
    return fruit
    

if __name__ == "__main__": # to test and run the API
    uvicorn.run(app, host="0.0.0.0", port=8000) # 8000 default  fr fastapi