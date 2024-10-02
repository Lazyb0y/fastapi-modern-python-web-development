import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic = HTTPBasic()


@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)):
    return {"username": creds.username, "password": creds.password}


if __name__ == "__main__":
    uvicorn.run("11_1_use_http_basic_auth_to_get_user_info:app", reload=True, port=8090)
