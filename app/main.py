from fastapi import FastAPI

from app.api import author,book,client
app = FastAPI()


# need to include route path here
#
# @app.on_event("startup")
# async def startup_db_client():
#     await database.connect()
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     await database.disconnect()

@app.get("/")
async def root():
    return {"status": "running"}

app.include_router(author.router, tags=["authors"])
app.include_router(book.router, tags=["books"])
app.include_router(client.router, tags=["clients"])

# app.include_router(author.router, prefix="/authors", tags=["authors"])
# app.include_router(book.router, prefix="/books", tags=["books"])
# app.include_router(client.router, prefix="/clients", tags=["clients"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
