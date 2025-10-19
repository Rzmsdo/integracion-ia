from fastapi import FastAPI
from ollama import generate, GenerateResponse
import uvicorn  


app = FastAPI()
 
@app.get("/")
async def read_root():
    response: GenerateResponse = generate("llama3.2", "¿sabes las diferencias entre una moneda y un billete?")
    print(response.response)
    return {"response": response.response}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
