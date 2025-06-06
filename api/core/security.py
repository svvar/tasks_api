import os
import asyncio
from datetime import timedelta, datetime, UTC

import jwt
from argon2 import PasswordHasher, Type
from dotenv import load_dotenv, find_dotenv
from fastapi import HTTPException, status, Header, Cookie

load_dotenv(find_dotenv())

"""
Won't use Oauth2 here, don't really need it and it forces to use 'username' as mandatory field, but I want to use
'email' field in /login form, so simple custom JWT-based auth is enough. 
JWT will be stored in cookies so testing via Swagger will be easy.
"""

JWT_ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1                   # 1 day

RSA_PRIVATE_KEY_PATH = os.getenv("RSA_PRIVATE_KEY_PATH") or os.getcwd() + "/rsa_private_key.pem" or None
RSA_PUBLIC_KEY_PATH = os.getenv("RSA_PUBLIC_KEY_PATH") or os.getcwd() + "/rsa_public_key.pem" or None
if not RSA_PRIVATE_KEY_PATH or not RSA_PUBLIC_KEY_PATH:
    exit("RSA_PRIVATE_KEY_PATH or RSA_PUBLIC_KEY_PATH not found in environment variables")

with open(RSA_PRIVATE_KEY_PATH, "r") as f:
    RSA_PRIVATE_KEY = f.read()

with open(RSA_PUBLIC_KEY_PATH, "r") as f:
    RSA_PUBLIC_KEY = f.read()

argon_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=32768,
    parallelism=4,
    hash_len=16,
    salt_len=16,
    type=Type.ID
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

expired_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired, please re-authenticate",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, RSA_PRIVATE_KEY, algorithm=JWT_ALGORITHM)


def get_current_user_id(
        access_token: str = Cookie(None),
        authorization: str = Header(None)
) -> int:
    if not access_token and authorization:
        if 'Bearer ' in authorization:
            access_token = authorization.split(' ')[1]
        else:
            raise credentials_exception

    payload = decode_access_token(access_token)
    id_ = payload.get("id")
    if id_ is None:
        raise credentials_exception
    return id_

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, RSA_PUBLIC_KEY, algorithms=[JWT_ALGORITHM], options={"verify_exp": True})
        return payload if payload else None
    except jwt.ExpiredSignatureError as e:
        raise expired_exception
    except jwt.PyJWTError as e:
        raise credentials_exception


async def get_password_argon_hash(password: str) -> str:
    # argon releases the GIL during hashing
    hashed = await asyncio.to_thread(argon_hasher.hash, password)
    return hashed


async def argon_verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        await asyncio.to_thread(argon_hasher.verify, hashed_password, plain_password)
        return True
    except Exception:
        return False