from fastapi import FastAPI

app = FastAPI()

# EP2
'''
# http://localhost:8080/
@app.get("/")
async def root():
    return {"message": "Hello Word"}

# http://localhost:8080/items/{item_id}?q={q}
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q" : q}
'''

# EP3
# part 1
'''
@app.get("/user/{user_id}")
async def get_users(user_id: int):
    return {"user_id": user_id}

@app.get("/user/me") # 將永遠執行不到
async def get_users():
    return {"user_id": "the current user"}
'''
# part 2
'''
from enum import Enum
class UserId(int, Enum):
    Alice = 1
    Bob = 2
    Eve = 3

@app.get("/user/{user_id}")
async def get_users(user_id: UserId):
    if user_id is UserId.Alice: # or "user_id == UserId.Alice"
        return {"user_id": user_id, "user_info": "someone who wants to send secret to Bob"}
    
    if user_id is 2:
        return {"user_id": user_id, "user_info": "someone who can access Alice's secret"}
    
    return {"user_id": user_id, "user_info": ""}
'''

# part 3
'''
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
'''

# EP4
'''
@app.get("/user/{user_id}/items/{item_id}")
												# Note: 若將預設值拿掉，則網址處必須輸入相對應數值，否則會報錯
async def get_users(user_id: int, item_id: int, q: int = 10, q2: int = 5):
    return {"user_id": user_id, "item_id": item_id, "q": q, "q2": q2}
'''
'''
from typing import Union
@app.get("/user/{user_id}")
async def get_users(user_id: int, q: Union[int,None]=None):
    return {"user_id": user_id, "q": q}
'''

# EP5
'''
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
'''
'''
@app.post("/items/")
async def create_item(item: Item):
    return item
'''
'''
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
'''
'''
@app.post("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
'''''
# EP6
'''
from typing import Annotated
from fastapi import Query, Path
#@app.get("/items")
#async def read_items(q: Annotated[str | None, Query(max_length=10, min_length=3, pattern="^fixedquery$")] = "default value"):
#																			Note: ^: start, $: end // 要求格式
#@app.get("/items")
#async def read_items(q: Annotated[str | None, Query(max_length=10, min_length=3, pattern="^fixedquery$")] = ...):
#																										Note: python 無法處理 ...
#@app.get("/items")
#async def read_items(q: Annotated[list[str] | None, Query(max_length=10, min_length=3)] = ["123", "456", "789"]):
#								  ^e.g. ?q=hello&q=world&q=20240926   			^在 list 中是去限制 list 內 element 的個數
#@app.get("/items")
#async def read_items(q: Annotated[list[int] | None, Query()] = [123, 456, 789]):
#@app.get("/items/")
#async def read_items(q: Annotated[str | None, Query(title="LYC", description="Query string for the items to search in the database that have a good match", min_length=3)] = None):
@app.get("/items/")
async def read_items(q: Annotated[str | None, 
                                  Query(
                                      title="LYC", 
                                      description="Query string for the items to search in the database that have a good match",
                                      alias="item-query",
                                    #  ^ 網址中用 alias 來取代 q, e.g. ?item-query=123
                                      deprecated=True,
                                    #  ^ 在 /docs 等 schema 上顯示 "deprecated(過時的)"
                                      include_in_schema=False)] = None):
    								#	^ 不會顯示在 /docs 等 schema 上
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
'''

# EP7
# part1
'''
from typing import Annotated
from fastapi import Path

@app.get("/items/{item_type}/{item_id}")
async def read_items(
	item_type: Annotated[str, Path(title="Type of item", max_length=10)],
 item_id: Annotated[int, Path(title="ID of item")],
):
    return {"type": item_type, "id": item_id}

@app.get("/items//{item_id}")
async def read_items_2(
	item_id: Annotated[int, Path(itile="ID of item")],
):
    return {"id": item_id, "message": "this is another endpoint"}
'''

# part2
'''
from typing import Annotated
from fastapi import Path
from decimal import Decimal

@app.get("/gtAndLt/{value}")
async def gt_and_lt(
	value: Annotated[Decimal, Path(gt=1, lt=10)]
):
    return {"value": value}

@app.get("/geAndLe/{value}")
async def ge_and_le(
	value: Annotated[Decimal, Path(ge=1, le=10)]
):
    return {"value": value}

@app.get("/multipleOf/{value}")
async def multiple_of(
	value: Annotated[Decimal, Path(multiple_of=0.5)]
):
    return {"value": value}

@app.get("/maxDigit/{value}")
async def max_digits(
	value: Annotated[Decimal, Path(max_digits=5)]
):
    return {"value": value}

@app.get("/dPlace/{value}")
async def decimal_places(
	value: Annotated[Decimal, Path(decimal_places=3)]
):
    return {"value": value}
'''

# Homework 2

# 1. GET "/" Endpoint
@app.get("/")
async def HW2_1():
    results = {"message": "Hello World"}
    return results
'''
# 2. PUT "/items/{item_id}" Endpoint
@app.put("/items/{item_id}")
async def HW2_2(item_id: int, q: str | None = None):
    results = {
		"item_id": item_id,
  		"name": "Test Item",
  		"description": "A test description",
		"price": 10.5,
  		"tax": 1.5
	}
    
    if q:
        results.update({"q": q})
    
    return results
'''
# Homework 3

# 1. GET /items/{item_id} Endpoint
from typing import Annotated
from fastapi import Path, Query
@app.get("/items/{item_id}")
async def HW3_1(
    item_id: Annotated[int, Path(ge=1, le=1000)], 
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None, 
    sort_order: str | None = "asc"):
    
    results = {"item_id": item_id}
    
    if q:
        results.update({"description": f"This is a sample item that matches the query {q}"})
    else:
        results.update({"description": "This is a sample item."})
    
    results.update({"sort_order": sort_order})
    
    return results

# 2. PUT "/items/{item_id}" Endpoint
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

@app.put("/items/{item_id}")
async def HW3_2(
    item_id: Annotated[int, Path(ge=1, le=1000)],
    item: Item,
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    
    results = {
		"item_id": item_id,
		**item.dict()
	}
    if q:
        results.update({"q": q})
    
    return results
