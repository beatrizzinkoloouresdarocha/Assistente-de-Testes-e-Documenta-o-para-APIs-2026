from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserRegister(BaseModel):
    username: str
    age: int


@app.post("/users/register")
def register_user(user: UserRegister):
    if user.age < 18:
        raise HTTPException(status_code=400, detail="Usuário deve ser maior de idade")
    return {"message": f"Usuário {user.username} cadastrado com sucesso!"}
