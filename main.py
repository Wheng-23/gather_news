import QingBao
import QingBao2
import QingBao3

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app1 = FastAPI()
origins = ["*"]

app1.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app1.include_router(QingBao.app)
app1.include_router(QingBao2.app)
app1.include_router(QingBao3.app)


if __name__ == "__main__":
    uvicorn.run(app="main:app1", host="127.0.0.1", port=8080, reload=True)