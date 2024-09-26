from fastapi import FastAPI, Depends, Query

app = FastAPI()


# the dependency function:
def check_dep(name: str = Query(None), password: str = Query(None)):
    if not name:
        raise


# the path function / web endpoint:
@app.get("/check_user", dependencies=[Depends(check_dep)])
def check_user() -> bool:
    return True
