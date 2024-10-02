import uvicorn
from fastapi import status, FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

secret_user: str = "newphone"
secret_password: str = "whodis?"

basic: HTTPBasicCredentials = HTTPBasic()


@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_password:
        return {"username": creds.username, "password": creds.password}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Hey! You are not authorized!"
    )


if __name__ == "__main__":
    uvicorn.run(
        "11_4_add_a_secret_username_and_password_to_auth:app", reload=True, port=8090
    )
