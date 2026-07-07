from fastapi import FastAPI,HTTPException,Depends
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

app = FastAPI()

#JWT Config
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 30



#Create Token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return token

@app.post("/login")
def logine(username:str,password:str):
    if username!="admin" or password!="1234":
        raise HTTPException(
            status_code=401,
            detail="invalid username or password"
        )
    token=create_token({
        "sub":username
    })
    return{
        "access_token":token
    }
def verify_token(token:str=Header(None)):
    
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="invalid or expired token"
        )
    
@app.get("/secure")
def secure_data(user=Depends(verify_token)):
    return{
        "message":"secure data accessed",
        "user":"admin"
    }
    
        



