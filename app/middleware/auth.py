from fastapi import FastAPI, Request, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.config import EnvironmentVariables

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@app.middleware("http")
async def jwt_auth_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        # Skip authentication for OPTIONS requests
        return await call_next(request)

    if any(request.url.path.startswith(path) for path in ["/auth", "/health", "/docs", "/redoc", "/openapi.json"]):
        response = await call_next(request)
        return response
    authHeader = request.headers.get('Authorization')
    print(authHeader);
    if not authHeader or 'Bearer ' not in authHeader:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authHeader.split("Bearer ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt.decode(token, EnvironmentVariables().SECRET_KEY, algorithms=[EnvironmentVariables().ALGORITHM])
        request.state.user_type = payload.get("user_type")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    response = await call_next(request)
    return response

