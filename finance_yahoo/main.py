from fastapi import FastAPI

from db import database, items

app = FastAPI()


@app.get("/items/")
async def get_items():
    query = items.select()
    return await database.fetch_all(query)


@app.get("/items/{item_id}")
async def get_item(item_id):
    query = items.select().where(items.c.company_id == item_id)
    return await database.fetch_all(query)
