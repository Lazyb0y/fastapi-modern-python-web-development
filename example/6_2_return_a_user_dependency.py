from fastapi import FastAPI, Depends, Query

app = FastAPI()


# the dependency function:
def user_dep(name: str = Query, password: str = Query):
    return {"name": name, "valid": True}


# the path function / web endpoint:
@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user


# GET /user?name=your_name&password=your_password
