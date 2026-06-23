import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.views import account
from app.admin import adminn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account)
app.include_router(adminn)


@app.get("/health")
def health_check():
    return Response("message: OK",status_code=200)







if __name__ == "__main__":
    uvicorn.run("manage:app",host='127.0.0.1',port=8000,reload=True)