import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import Response



app = FastAPI()



@app.get("/health")
def health_check():
    return Response("message: OK",status_code=200)







if __name__ == "__main__":
    uvicorn.run("manage:app",host='127.0.0.1',port=8000,reload=True)