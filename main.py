from fastapi import FastAPI

app = FastAPI()

# region EP.2:
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
#endregion

# region EP.3:
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
#endregion

# region EP.4:
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
#endregion

# region EP.5:
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
'''
#endregion

# region EP.6:
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
									dEP.recated=True,
									#  ^ 在 /docs 等 schema 上顯示 "dEP.recated(過時的)"
									include_in_schema=False)] = None):
									#	^ 不會顯示在 /docs 等 schema 上
	results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
	if q:
		results.update({"q": q})
	return results
'''
# endregion

# region EP.7:
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
# endregion

# region Homework2:
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
# endregion

# region Homework3:

# region 1. GET /items/{item_id} Endpoint

from typing import Annotated
from fastapi import Path, Query
@app.get("/items/{item_id}")
async def HW3_1(
	item_id: Annotated[int, Path(ge=1, le=1000)], 
	q: Annotated[str | None, Query(min_length=3, max_length=50)] = None, 
	sort_order: str | None = "asc"):
	
	results = {"item_id": item_id, "description": "This is a sample item.", "sort_order": sort_order}
	
	if q:
		results.update({"description": f"This is a sample item that matches the query {q}"})

	return results
# endregion

# region 2. PUT "/items/{item_id}" Endpoint

from pydantic import BaseModel

class Item_HW3(BaseModel):
	name: str
	description: str
	price: float
	tax: float


@app.put("/items/{item_id}")
async def HW3_2(
	item_id: Annotated[int, Path(ge=1, le=1000)],
	item: Item_HW3,
	q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
	
	results = {
		"item_id": item_id,
		**item.dict()
	}
	if q:
		results.update({"q": q})
	
	return results
# endregion
# endregion

# region EP.8 Body - MultiplParameters:

# region 	Part1
'''
from typing import Annotated
from fastapi import Path
from pydantic import BaseModel
class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
	item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
	q: str | None = None,
	item: Item | None = None,
):
	results = {"item_id": item_id}
	if q:
		results.update({"q": q})
	if item:
		results.update({"item": item})
	return results
'''
# endregion

# region 	Part2
'''
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


class User(BaseModel):
	username: str
	full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
	results = {"item_id": item_id, "item": item, "user": user}
	return results
'''
# endregion

# region 	Part3
'''
from typing import Annotated
from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


class User(BaseModel):
	username: str
	full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
	item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
	results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
	return results
'''
# endregion

# region 	Part4
'''
from typing import Annotated
from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


class User(BaseModel):
	username: str
	full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
	*,
	item_id: int,
	item: Item,
	user: User,
	importance: Annotated[int, Body(gt=0)],
	q: str | None = None,
):
	results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
	if q:
		results.update({"q": q})
	return result
'''
# endregion

# region 	Part 5
'''
from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


@app.put("/items/{item_id}")
#																即使只有一個 body parameter, 使用 embed=True 時 FastAPI 會預期給入此餐醋的名字(觀察 doc 可發現 request body 中顯示出此 body 的名字
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion
# endregion

# region EP.9 Body - Fields:
'''
from typing import Annotated
from fastapi import Body
from pydantic import BaseModel, Field
# 								(new)
# The same way you can declare additional validation and metadata in path operation function parameters with Query, 
# Path and Body, you can declare validation and metadata inside of Pydantic models using Pydantic's Field.

class Item(BaseModel):
	name: str
	description: str | None = Field(
		default=None, title="The description of the item", max_length=10
	)
	price: float = Field(gt=0, description="The price must be greater than zero")
	tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region EP.10 Body - Nested Models:

# region 	Part 1. List fields
'''
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: list = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 2. List fields with type parameter
'''
from typing import List, Union
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: Union[str, None, int] = None
	price: float
	tax: Union[float, None] = None
	tags: List[str] = [] # 允許重複的名字


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 3. Set types
# But then we think about it, and realize that tags shouldn't repeat, they would probably be unique strings.
# And Python has a special data type for sets of unique items, the set.
'''
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: set[str] = set() # unique items


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 4. Nested Models
# Each attribute of a Pydantic model has a type.
# But that type can itself be another Pydantic model.
# So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.
# All that, arbitrarily nested. 
# (把一個 model 塞進另一個 model)
'''
from pydantic import BaseModel

class Image(BaseModel):
	url: str # Note: 雖然名稱是 url 卻沒有限制輸入，將導致不如預期。見下一 Part 改善
	name: str


class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: set[str] = set()
	image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 5. Special types and validation
# Apart from normal singular types like str, int, float, etc. you can use more complex singular types that inherit from str.
# To see all the options you have, checkout Pydantic's Type Overview (https://docs.pydantic.dev/latest/concepts/types/).
'''
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
	url: HttpUrl # 限制型別為 http url
	name: str


class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: set[str] = set()
	image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 6. Attributes with lists of submodels
'''
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
	url: HttpUrl
	name: str


class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: set[str] = set()
	images: list[Image] | None = None
	# 		list of models


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 7. Deeply nested models
'''
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
	url: HttpUrl
	name: str


class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: set[str] = set()
	images: list[Image] | None = None


class Offer(BaseModel):
	name: str
	description: str | None = None
	price: float
	items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
	return offer
'''
# endregion

# region 	Part 8. Bodies of pure lists
'''
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
	url: HttpUrl
	name: str


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
	return images
'''
# endregion

# 			Part 9. Editor support everywhere
# region 	Part 10. Bodies of arbitrary dicts
'''
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
	return weights
'''
# endregion

# endregion

# region EP.11 Declare Request Example Data:

# region 	Part 1. Extra JSON Schema data in Pydantic models
# You can declare examples for a Pydantic model that will be added to the generated JSON Schema.
'''
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None

	# 對當前 model 用 jason 來設定預設值
	model_config = {
		"json_schema_extra": {
			"examples": [
				{
					"name": "Foo",
					"description": "A very nice Item",
					"price": 35.4,
					"tax": 3.2,
				}
			]
		}
	}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 2. Field additional arguments
# 以下例子會產生與 Part 1. 相同的結果
'''
from pydantic import BaseModel, Field

class Item(BaseModel):
	name: str = Field(examples=["Foo"])
	description: str | None = Field(default=None, examples=["A very nice Item"])
	price: float = Field(examples=[35.4])
	tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# examples in JSON Schema - OpenAPI
# When using any of:
# 	Path()
# 	Query()
# 	Header()
# 	Cookie()
# 	Body()
# 	Form()	
# 	File()
# you can also declare a group of examples with additional information that will be added to their JSON Schemas inside of OpenAPI.

# region 	Part 3. Body with examples
'''
from typing import Annotated
from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
	item_id: int,
	item: Annotated[
		Item,
		Body(
			examples=[
				{
					"name": "Foo",
					"description": "A very nice Item",
					"price": 35.4,
					"tax": 3.2,
				},
				#{
				#    "name": "Bar",
				#    "price": "35.4",
				#},
				#{
				#    "name": "Baz",
				#    "price": "thirty five point four",
				#},
				# Note: examples 其實支援多個範例的撰寫。
				# 		Nevertheless, at the time of writing this, Swagger UI, the tool in charge of showing the docs UI, 
				# 		doesn't support showing multiple examples for the data in JSON Schema. But read below for a workaround.
			],
		),
	],
):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion

# region 	Part 4. OpenAPI-specific examples - Using the openapi_examples Parameter
# This OpenAPI-specific examples goes in another section in the OpenAPI specification. 
# It goes in the details for each path operation, not inside each JSON Schema.
# And Swagger UI has supported this particular examples field for a while. 
# So, you can use it to show different examples in the docs UI.
# The shape of this OpenAPI-specific field examples is a "dict" with multiple examples (instead of a list), each with extra information that will be added to OpenAPI too.
# This doesn't go inside of each JSON Schema contained in OpenAPI, this goes outside, in the path operation directly.
'''
from typing import Annotated
from fastapi import Body
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
	*,
	item_id: int,
	item: Annotated[
		Item,
		Body(
			openapi_examples={
				# Each specific example dict in the examples can contain:
				# 	summary: Short description for the example.
				# 	description: A long description that can contain Markdown text.
				# 	value: This is the actual example shown, e.g. a dict.
				# 	externalValue: alternative to value, a URL pointing to the example. Although this might not be supported by as many tools as value.
				"normal": {
					"summary": "A normal example",
					"description": "A **normal** item works correctly.",
					"value": {
						"name": "Foo",
						"description": "A very nice Item",
						"price": 35.4,
						"tax": 3.2,
					},
				},
				"converted": {
					"summary": "An example with converted data",
					"description": "FastAPI can convert price `strings` to actual `numbers` automatically",
					"value": {
						"name": "Bar",
						"price": "35.4",
					},
				},
				"invalid": {
					"summary": "Invalid data is rejected with an error",
					"value": {
						"name": "Baz",
						"price": "thirty five point four",
					},
				},
			},
		),
	],
):
	results = {"item_id": item_id, "item": item}
	return results
'''
# endregion
# endregion

# region EP.12 Extra Data Types:
# Pydantic types: https://docs.pydantic.dev/latest/concepts/types/
'''
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID # Universally Unique Identifier 通用唯一識別碼 (128 bits)
from fastapi import Body

@app.put("/items/{item_id}")
async def read_items(
	item_id: UUID,
	start_datetime: Annotated[datetime, Body()],
	end_datetime: Annotated[datetime, Body()],
	process_after: Annotated[timedelta, Body()],
	repeat_at: Annotated[time | None, Body()] = None,
):
	start_process = start_datetime + process_after
	duration = end_datetime - start_process
	return {
		"item_id": item_id,
		"start_datetime": start_datetime,
		"end_datetime": end_datetime,
		"process_after": process_after, # example: P3D(Period of 3 days)
		"repeat_at": repeat_at,
		"start_process": start_process,
		"duration": duration,
	}
'''
# endregion

# region EP.13&14 Cookie Parameters & Header Parameters:

# region 	Part 1. Cookie Parameters
'''
from typing import Annotated
from fastapi import Cookie

@app.get("/example/")
async def read_example(
	yummy_cookie: Annotated[str | None, Cookie()] = None
):
	return {"yummy_cookie": yummy_cookie}

# Note: Swagger UI 因安源疑慮，UI 中並不會顯示 cookie 設定的結果(會顯示 null)．
# 		若想看結果可將其 Responses 中 Curl 的內容複製到 Terminal 執行，便可查看執行結果
'''
# endregion

# region 	Part 2. Header Parameters
'''
from typing import Annotated
from fastapi import Cookie, Header

@app.get("/example/")
async def read_example(
	yummy_cookie: Annotated[str | None, Cookie()] = None,
	user_agent: Annotated[str | None, Header()] = None,
):
	return {"yummy_cookie": yummy_cookie, "user_agent": user_agent}
'''
# endregion

# region 	Part 3. Header Parameters - Automatic conversion
# Header has a little extra functionality on top of what Path, Query and Cookie provide.
# Most of the standard headers are separated by a "hyphen" character, also known as the "minus symbol" (-).
# But a variable like user-agent is invalid in Python.
# So, by default, Header will convert the parameter names characters from underscore (_) to hyphen (-) to extract and document the headers(自動將 "_" 轉換為 "-").
# Also, HTTP headers are "case-insensitive"(不區分大小寫), so, you can declare them with standard Python style (also known as "snake_case").
# So, you can use user_agent as you normally would in Python code, instead of needing to capitalize the first letters as User_Agent or something similar.
# If for some reason you need to disable automatic conversion of underscores to hyphens, set the parameter convert_underscores of Header to False
# (若想取消自動轉換可下 convert_underscores=False)
'''
from typing import Annotated
from fastapi import Cookie, Header

@app.get("/example/")
async def read_example(
	yummy_cookie: Annotated[str | None, Cookie()] = None,
	user_agent: Annotated[str | None, Header(convert_underscores=False)] = None,
):
	return {"yummy_cookie": yummy_cookie, "user_agent": user_agent}
'''
# endregion

# region 	Part 4. Header Parameters - Duplicate Headers
'''
from typing import Annotated
from fastapi import Cookie, Header

@app.get("/example/")
async def read_example(
	yummy_cookie: Annotated[str | None, Cookie()] = None,
	user_agent: Annotated[str | None, Header()] = None,
	x_token: Annotated[list[str] | None, Header()] = None,
):
	return {"yummy_cookie": yummy_cookie, "user_agent": user_agent, "x_token": x_token}
'''
# endregion
# endregion

# region Homework4:

# region 1. POST /items/filter/

from typing import Annotated
from fastapi import Query

@app.post("/items/filter/")
async def HW4_1(
	price_min: Annotated[int, Query()],
	price_max: Annotated[int, Query()],
	tax_included: Annotated[bool, Query()],
	tags: Annotated[list[str], Query()]
):
	results = {
		"price_range": [price_min, price_max],
		"tax_included": tax_included,
		"tags": tags,
		"message": "This is a filtered list of items based on the provided criteria."
	}
	return results
# endregion

# region 2. POST /items/create_with_fields/

from pydantic import BaseModel, Field
from fastapi import Body
class Item_HW4(BaseModel):
	name: str
	description: str = Field(title="The description of the item")
	price: float = Field(gt=0, description="The price must be greater than zero")
	tax: float

@app.post("/items/create_with_fields/")
async def HW4_2(
    item: Annotated[Item_HW4, Body()], 
    importance: Annotated[int, Body()]
):
	return {"item": item, "importance": importance}
# endregion

# region 3. POST /offers/

class Offer_HW4(BaseModel):
	name: str = Field(title="The name of the offer")
	discount: float = Field(title="The discount percentage for the offer")
	items: list[Item_HW4] = Field(title="A list of items included in the offer")

@app.post("/offers/")
async def HW4_3(offer_data: Annotated[Offer_HW4, Body()]):
	return {"offer_name": offer_data.name, "discount": offer_data.discount, "items": offer_data.items}
# endregion

# region 4. /users/

class User_HW4(BaseModel):
	username: str = Field(title="Username of the user")
	email: str = Field(default="helloworld@example.com", title="Email address of the user", pattern="[^@]+@[^@]+\.[^@]+")
	full_name: str = Field(title="Full name of the user")

@app.post("/users/")
async def HW4_4(user: Annotated[User_HW4, Body()]):
	return user
# endregion

# region 5. POST /items/extra_data_types/

from typing import Annotated
from datetime import datetime, time, timedelta
from fastapi import Body
from uuid import UUID
@app.post("/items/extra_data_types/")
async def HW4_5(
	start_time: Annotated[datetime, Body()],
	end_time: Annotated[time, Body()],
	repeat_every: Annotated[timedelta, Body()],
	process_id: Annotated[UUID, Body()]
):
    return {"message": "This is an item with extra data types.", "start_time": start_time, "end_time": end_time, "repeat_every": repeat_every, "process_id": process_id}
# endregion

# region 6. GET /items/cookies/

from fastapi import Cookie

@app.get("/items/cookies/")
async def HW4_6(
	session_id: Annotated[str | None, Cookie()] = None
):
    return {"session_id": session_id, "message": "This is the session ID obtained from the cookies."}
# endregion
# endregion

# region EP.15 Response Model - Return Type:

# region Part 1. Return type annotation
'''
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	tags: list[str] = []

@app.post("/items/")
async def create_item(item: Item) -> Item:
	return item

@app.get("/items/")
async def read_items() -> list[Item]:
	return [
		Item(name="Portal Gun", price=42.0),
		Item(name="Plumbus", price=32.0),
	]
'''
# endregion

# region Part 2. 跟 Validate 有關的補充
'''
from pydantic import BaseModel

class PydanticObject(BaseModel):
	data: int
	data2: bool | None = None

class CustomObject:
	def __init__(self, data: int, data2: bool | None = None):
		self.data = data
		self.data2 = data2

@app.get("/example")
def example_endpoint(mode: int | None = 0) -> PydanticObject:
	if mode == 0:
		res = PydanticObject(data=123, data2=True) # valid
	elif mode == 1:
		res = PydanticObject(data="123", data2="True") # valid, "123" can be converted to int, "True" can be converted to bool
	elif mode == 2:
		res = PydanticObject(data="abc", data2="True") # invalid, "abc" cannot be converted to int
	elif mode == 3:
		res = PydanticObject(data=123) # valid, data2 is optional
	elif mode == 4:
		res = PydanticObject(data2=True) # invalid, data is required
	elif mode == 5:
		res = {"data": 123, "data2": True} # valid, Pydantic model can be constructed from dict. 
		# Keys is matched with the model's field names
	elif mode == 6:
		res = {"data": 123, "data2": True, "extra": "extra"} # valid, extra is ignored
	elif mode == 7:
		res = {"extra": "extra"} # invalid, data is required but key name "data" isn't found in the dict
	elif mode == 8:
		res = CustomObject(data=123, data2=True) # valid, Pydantic model can be constructed from python object
		# Object's attributes is matched with the model's field names
	elif mode == 9:
		res = [123, True] # invalid, Pydantic model can't be constructed from list
	return res
'''
# endregion

# region Part 3. Response model
'''
from typing import Any

from pydantic import BaseModel


class Item_EP15(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item_EP15)
async def create_item(item: Item_EP15) -> Any:
    return item


@app.get("/items/", response_model=list[Item_EP15])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
'''
# endregion

# region Part 4. Filtering data
'''
from pydantic import BaseModel

class User_EP15(BaseModel):
    username: str
    userID: int
    userEmail: str
    password: str
    
def getUserFromDB(username: str) -> User_EP15:
    # This is a dummy function to simulate a database query
    # You must imagine that this function is querying a database, and transforming the result into User model instance
    return User_EP15(username=username, userID=1, userEmail="hi@example.com", password="yourpassword")

@app.get("/user/{username}")
async def read_user(username: str) -> User_EP15:
    return getUserFromDB(username) # really bad

class UserOut_EP15(BaseModel):
    username: str
    userID: int
    userEmail: str
    password: str

@app.get("/user2/{username}", response_model=UserOut_EP15)
async def read_user2(username: str) -> User_EP15:
    return getUserFromDB(username)
'''
# endregion

# region Part 5. Filtering data by inheritance
'''
from pydantic import BaseModel

class baseUser_EP15(BaseModel):
    username: str
    userID: int
    userEmail: str
    
class fullUser_EP15(baseUser_EP15): # inherit from baseUser
    password: str
    
def getUserFromDB(username: str) -> fullUser_EP15:
    return fullUser_EP15(username=username, userID=1, userEmail="hi@example.com", password="yourpassword")

@app.get("/user/{username}")
async def read_user(username: str) -> baseUser_EP15:
    return getUserFromDB(username) # return type is baseUser, but returning fullUser instance
'''
# endregion

# region Part 6. Other Return type
'''
from fastapi import Response
from fastapi.responses import JSONResponse, RedirectResponse

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(status_code=404, content={"message": "Here's your interdimensional portal."})
'''
# endregion

# region Part 7. Invalid Return Type
'''
from pydantic import BaseModel

class DatabaseObject:
    def __init__(self, data: str):
        self.data = data

class DatabaseModel(BaseModel):
    data: str

# uncomment below endpoint, and fastAPI will be failed to start

# @app.get("/example-fail")
# def fail_endpoint() -> DatabaseObject:
#     return DatabaseObject(data="some data")

@app.get("/example-success", response_model=DatabaseModel)
def success_endpoint() -> DatabaseObject:
    return DatabaseObject(data="some data")
'''
# endregion

# region Part8. Response Model encoding parameters
'''
from pydantic import BaseModel

class Item_EP15(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2, "tags": ["tag1", "tag2"]},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/ex-unset/{item_id}", response_model=Item_EP15, response_model_exclude_unset=True)
async def exclude_unset(item_id: str):
    return items[item_id]

@app.get("/ex-default/{item_id}", response_model=Item_EP15, response_model_exclude_defaults=True)
async def exclude_defaults(item_id: str):
    return items[item_id]

@app.get("/ex-none/{item_id}", response_model=Item_EP15, response_model_exclude_none=True)
async def exclude_none(item_id: str):
    return items[item_id]

@app.get("/include/{item_id}", response_model=Item_EP15, response_model_include={"name", "description"})
async def include_fields(item_id: str):
    return items[item_id]

@app.get("/exclude/{item_id}", response_model=Item_EP15, response_model_exclude=["tax", "tags"])
async def exclude_fields(item_id: str):
    return items[item_id]
'''
# endregion

# endregion

# region EP.16 Extra Models
#- 考慮以下情境：
#    - 我們提供一個 POST endpoint，`create_user`
#        - Client 可以透過 Request body 傳入帳號密碼
#        - API 用帳號密碼等資訊創造 User，並存入 Database
#        - API 最後將 User 在 DB 中的資訊，過濾掉密碼之後，response 給 Client
#    - 我們需要三個 model：
#        - `UserIn` 作為 Clinet 傳入 User 資訊的 model
#            - 有帳號，明文密碼，Email
#        - `UserInDB` 作為 DB 儲存 User 資訊的 model
#            - 有帳號，雜湊密碼，Email，User ID
#        - `UserOut` 作為 API 的 Response model
#            - 有帳號，Email，User ID

# region 	Part 1. Multiple Models
'''
from pydantic import BaseModel, EmailStr, Field
import random

class UserIn_EP16_1(BaseModel):
    username: str
    password: str
    email: str = Field(default="helloworld@example.com", pattern="[^@]+@[^@]+\.[^@]+") # Emailstr cannot work

class UserOut_EP16_1(BaseModel):
    username: str
    email: str = Field(default="helloworld@example.com", pattern="[^@]+@[^@]+\.[^@]+") # Emailstr cannot work
    id: int

class UserInDB_EP16_1(BaseModel):
    username: str
    hashed_password: str
    email: str = Field(default="helloworld@example.com", pattern="[^@]+@[^@]+\.[^@]+") # Emailstr cannot work
    id: int

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn_EP16_1):
    hashed_password = fake_password_hasher(user_in.password)
    id = random.randint(1, 1000)
    user_in_db = UserInDB_EP16_1(**user_in.dict(), hashed_password=hashed_password, id=id)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut_EP16_1)
async def create_user(user_in: UserIn_EP16_1):
    user_saved = fake_save_user(user_in)
    return user_saved
'''
# endregion 

# region 	Part 2. Reduce duplication
'''
from pydantic import BaseModel, EmailStr, Field
import random

class UserBase_EP16_2(BaseModel):
    username: str
    email: str = Field(default="helloworld@example.com", pattern="[^@]+@[^@]+\.[^@]+") # Emailstr cannot work

class UserIn_EP16_2(UserBase_EP16_2):
    password: str

class UserOut_EP16_2(UserBase_EP16_2):
    id: int

class UserInDB_EP16_1(UserBase_EP16_2):
    hashed_password: str
    id: int

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn_EP16_2):
    hashed_password = fake_password_hasher(user_in.password)
    id = random.randint(1, 1000)
    user_in_db = UserInDB_EP16_1(**user_in.dict(), hashed_password=hashed_password, id=id)
    print("User saved! ..not really")
    return user_in_db

@app.post("/user/", response_model=UserOut_EP16_2)
async def create_user(user_in: UserIn_EP16_2):
    user_saved = fake_save_user(user_in)
    return user_saved
'''
# endregion

# region 	Part 3. Union
'''
from typing import Union
from pydantic import BaseModel

class BaseItem_EP16_3(BaseModel):
    description: str
    type: str

class CarItem_EP16_3(BaseItem_EP16_3):
    type: str = "car"

class PlaneItem_EP16_3(BaseItem_EP16_3):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "a car", "type": "car"},
    "item2": {
        "description": "a plane",
        "type": "plane",
        "size": 5,
    },
}

														# Pydantic v1: check the list in order from left to right
														# Pydantic v2: smart mode (don't care the order)
@app.get("/items_EP16_3/{item_id}", response_model=Union[PlaneItem_EP16_3, CarItem_EP16_3])
async def read_item(item_id: str):
    return items[item_id]
'''
# endregion

# region 	Part 4. List of models
'''
from pydantic import BaseModel

class Item_EP16_4(BaseModel):
    name: str
    description: str

items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
    # {"name": "Blue"} # invalid
]

@app.get("/items_EP16_4/", response_model=list[Item_EP16_4])
async def read_items():
    return items
'''
# endregion

# region 	Part 5. Response with arbitrary `dict`
'''
from fastapi import FastAPI

app = FastAPI()

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
'''
# endregion

# endregion

# region EP.17 Response Status Code

# region 	Part 1. Response Status Code
'''
from http import HTTPStatus

@app.post("/items_EP17_1/", status_code=HTTPStatus.ACCEPTED)
async def create_item(name: str):
    return {"name": name}
'''
# endregion

# region 	Part 2. Shortcut to remember the names
'''
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
'''
# endregion

# endregion

# region EP.18 Form Data
'''
from typing import Annotated
from fastapi import Form

@app.post("/login/")
						# 一般(未使用 Form)是用 jason 傳資料, 此處的 From 會使用 x-www-form-urlencoded 的方式傳輸資料
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
'''
# endregion

# region EP.19 Request Files

# region 	Part 1.
'''
from typing import Annotated

from fastapi import File, UploadFile

# Define File Parameters
@app.post("/files/")
									# recommend for small file
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

# File Parameters with UploadFile
@app.post("/uploadfile/")
							# upload limit info, recommend for large file
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
'''
# endregion

# region 	Part 2. Optional File Upload
'''
from typing import Annotated
from fastapi import File, UploadFile

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
'''
# endregion

# region 	Part 3. UploadFile with Additional Metadata
'''
from typing import Annotated
from fastapi import File, UploadFile

@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}
'''
# endregion

# region 	Part 4. Multiple File Uploads
'''
from typing import Annotated
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse

@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/EP19_4/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
'''
# endregion

# region 	Part 5. Multiple File Uploads with Additional Metadata
'''
from typing import Annotated
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse


@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}


@app.get("/EP19_5")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
'''
# endregion

# endregion

# region EP.20 Request Forms and Files
'''
from typing import Annotated
from fastapi import File, Form, UploadFile

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
'''
# endregion

# region EP.21 Handling Errors

# region 	Part 1. Use HTTPException
'''
from fastapi import HTTPException

items = {"foo": "The Foo Wrestlers"}

@app.get("/items_EP21_1/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
'''
# endregion

# region 	Part 2. Add custom headers
'''
from fastapi import HTTPException

items = {"foo": "The Foo Wrestlers"}

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}
'''
# endregion

# region 	Part 3. Install custom exception handlers
'''
from fastapi import Request
from fastapi.responses import JSONResponse

class UnicornException_EP21_3(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException_EP21_3)
async def unicorn_exception_handler(request: Request, exc: UnicornException_EP21_3):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException_EP21_3(name=name)
    return {"unicorn_name": name}
'''
# endregion

# region 	Part 4. Override the default exception handlers
'''
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Override the HTTPException error handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Override request validation exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    #return PlainTextResponse(str(exc), status_code=400)
	return PlainTextResponse(str(exc.errors()[0]['msg']), status_code=400)


@app.get("/items_EP21_4/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
'''
# endregion

# region 	Part 5. Use the RequestValidationError body
'''
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item_EP21_5(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item_EP21_5):
    return item
'''
# endregion

# region 	Part 6. Reuse FastAPI's exception handlers
'''
from fastapi import HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items_EP21_6/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
'''
# endregion

# endregion

# region Homework5

from typing import Annotated
from fastapi import Form, UploadFile, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.post("/items/form_and_file/")
async def HW5(
	name: Annotated[str, Form(title="The name of the item.")],
 	price: Annotated[float, Form(title="The price of the item.")],
	file: UploadFile | None = None,
	description: Annotated[str | None, Form(title="A description of the item.")] = None,
	tax: Annotated[float | None, Form(title="The applicable tax for the item.")] = None
):
    if price < 0:
        raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
   			detail="Price cannot be negative",
		)
    
    if not file:
        raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
   			detail="The file is missing",
		)
    
    results = {"name": name, "price": price, "filename": file.filename, "message": "This is an item created using form data and a file."}
    if description:
        results.update({"description": description})
    if tax:
        results.update({"tax": tax})
    return results

# endregion

# region EP.22 Path Operation Configuration

# region 	Part 1. Tags
'''
@app.post("/items/", tags=["items"])
async def create_item(item: str):
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return "some items"

@app.get("/users/", tags=["users"])
async def read_users():
    return "some users"

@app.put("/user/items", tags=["users", "items"])
async def add_items_for_user():
    return "item of user"
'''
# endregion

# region 	Part 2. Tags with Enums
'''
from enum import Enum

class Tags_EP22_2(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags_EP22_2.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Tags_EP22_2.users])
async def read_users():
    return ["Rick", "Morty"]
'''
# endregion

# region 	Part 3. Summary and description
# function name will be showed in docs title if there is no summary set
'''
@app.get("/")
async def path_operation_with_no_summary():
    return {"msg": "Hello World"}

@app.post(
    "/items/",
    summary="Create an item",
    description="Create an item from user provided string",
)
async def create_item(item: str):
    return item
'''
# endregion

# region	Part 4. Description from docstring
'''
from pydantic import BaseModel

class Item_EP22_4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items/", response_model=Item_EP22_4, summary="Create an item")
async def create_item(item: Item_EP22_4):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """ # Note: 這非省略
    return item
'''
# endregion

# region	Part 5. Response description
'''
from pydantic import BaseModel

class Item_EP22_5(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post(
    "/items/",
    response_model=Item_EP22_5,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item_EP22_5):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item
'''
# endregion

# region	Part 6. Deprecate a operation
'''
@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
'''
# endregion

# endregion

# region EP.23 JSON Compatible Encoder
'''
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}

class Item_EP23(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.post("/items/{id}")
async def update_item(id: str, item: Item_EP23):
    print(item)
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    fake_db[id] = json_compatible_item_data
    return json_compatible_item_data
'''
# endregion

# region EP.24 Body - Updates

# region 	Part 1. Update replacing with PUT
'''
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Item_EP24_1(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items_EP24/{item_id}", response_model=Item_EP24_1)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items_EP24/{item_id}", response_model=Item_EP24_1)
async def update_item(item_id: str, item: Item_EP24_1):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
'''
# endregion

# region 	Part 2. Partial updates with PATCH
'''
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Item_EP24_2(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items_EP24_2/{item_id}", response_model=Item_EP24_2)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/items_EP24_2/{item_id}", response_model=Item_EP24_2)
async def update_item(item_id: str, item: Item_EP24_2):
    stored_item_data = items[item_id]
    stored_item_model = Item_EP24_2(**stored_item_data) # MyPy marks it as an error but it doesn't
    update_data = item.dict(exclude_unset=True) # dict --new-version-> model_dump
    updated_item = stored_item_model.copy(update=update_data) # copy --new-version-> model_copy
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
'''
# endregion

# endregion

# region Homework6
from pydantic import Field

class Author(BaseModel):
    name: str
    age: int = Field(ge=0)

class Book(BaseModel):
    title: str
    author: Author
    summary: str | None = None

books = [
	{"title": "Book 1", "author": {"name": "Author 1", "age": 30}, "summary": "I am Taiwanese"},
	{"title": "Book 2", "author": {"name": "Author 2", "age": 40}, "summary": "I am Taiwanese 2"}
]

# region 1. GET /books/
# Description: Create an endpoint to retrieve a list of books with details such as the title, author, and summary.
@app.get("/books/")
async def HW6_1_get_books(
    book_id: int | None = None
):
    if book_id:
        if book_id > len(books):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "The book is not exit."}
            )
        return books[book_id - 1]
    return books
# endregion

# region 2. POST /books/create_with_author/
# Description**: Create an endpoint that allows adding a book with its author details.
from fastapi.encoders import jsonable_encoder
@app.post("/books/create_with_author/", response_model=Book)
async def HW6_2_adding_book_with_it_author(
	new_book_with_author_info: Book
):
    jsonable_encoder_book_data = jsonable_encoder(new_book_with_author_info)
    book_id = len(books)
    books.insert(book_id, jsonable_encoder_book_data)
    return new_book_with_author_info
# endregion

# region 3. POST /books/
@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def HW6_3_create_a_new_book(
	new_book: Book
):
    jsonable_encoder_book_data = jsonable_encoder(new_book)
    book_id = len(books)
    books.insert(book_id, jsonable_encoder_book_data)
    return new_book
# endregion

# endregion
