from fastapi import FastAPI , Query,Path,Depends,Body,Cookie,status,Form,File,UploadFile,HTTPException,Request,status,Header
from fastapi import Depends                                                                                                                                                                                                                         
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime, time, timedelta                                                                                                                                                                                                                                                                                                                      
from typing import Annotated,List, Optional,Any,Union
from enum import Enum
from pydantic import BaseModel,Field
from uuid import UUID
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}



#-------Path Parameters---------


# Ví dụ: truy cập thông tin của một mặt hàng theo item_id                                                                                                       
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}                 

@app.get("/users/{user_id}/orders/{order_id}")
async def read_order(user_id: int, order_id: int):                   
    return {"user_id": user_id, "order_id": order_id}



# ví dụ về sử dụng Enum để định nghĩa các mô hình
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"



@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#-------Query Parameters---------

#ví dụ về sử dụng query parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# ví dụ về Optional parameters 

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

#ví dụ về Query parameter type conversion 


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#-------Request Body----------


# Định nghĩa cấu trúc dữ liệu cho request body
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

app = FastAPI()

# API nhận dữ liệu từ request body
@app.post("/items/")
async def create_item(item: Item):
    return {
        "message": "Item received",
        "item": item
    }

#-----Query Parameters and String Validations----
# giup xác định các ràng buộc cho các tham số truy vấn (query parameters) như độ dài tối thiểu, tối đa, mẫu regex, v.v.
@app.get("/search/")
def search_item(q: str = Query(min_length=3, max_length=10)):
    return {"q": q}

@app.get("/users/")
def get_user(username: str = Query(pattern="^[a-zA-Z0-9_]+$")):
    return {"username": username}

@app.get("/alias/")
def get_item(keyword: str = Query(alias="search-keyword")):
    return {"keyword": keyword}

@app.get("/default/")
def get_item(q: str = Query(default="Minh anh ")):
    return {"q": q}

@app.get("/products/")
def get_product(
    name: str = Query(min_length=2, max_length=20, description="Tên sản phẩm", title="Tên")
):
    return {"name": name}

@app.get("/include_in_schema/")
def read_items(hidden_param: str = Query(default="secret", include_in_schema=False)):
    return {"hidden_param": hidden_param}

#-------Path Parameters and Numeric Validations---------
#giup xác định các ràng buộc cho các tham số đường dẫn (path parameters) như giá trị tối thiểu, tối đa, v.v.
@app.get("/Numeric_Validations/{item_id}")
def read_item(
    item_id: int = Path(..., title="ID của item", ge=1, le=1000)
):
    return {"item_id": item_id}

#-------Query Parameter Models---------
# Sử dụng Pydantic để định nghĩa các mô hình cho các tham số truy vấn (query parameters)
class FilterParams(BaseModel):
    keyword: str | None = None
    page: int = 1
    limit: int = 10

@app.get("/Parameter_Models")
def search_items(params: FilterParams = Depends()):
    return {
        "keyword": params.keyword,
        "page": params.page,
        "limit": params.limit
    }

#-------Body - Multiple Parameters--------
# Sử dụng Pydantic để định nghĩa các mô hình cho các tham số trong body


#-------Mix Path, Query and body parameters---------
# Sử dụng Pydantic để định nghĩa các mô hình cho các tham số trong body, kết hợp với các tham số đường dẫn (path parameters) và truy vấn (query parameters)
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/Multiple_Parameters/{item_id}")
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

#-------Singular values in body---------
# giup nhận các giá trị đơn lẻ trong body của yêu cầu HTTP, thay vì một đối tượng phức tạp
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/Singular_values_in_body/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

#-------Multiple body params and query----------
# Sử dụng nhiều tham số body và truy vấn trong một API
class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.post("/Multiple_body_params_and_query/")
async def create_item(
    item: Item,
    user: User,
    importance: int = Query(default=1)
):
    return {
        "item": item,
        "user": user,
        "importance": importance
    }
#-------Embed_a_single_body_parameter----------
# bat nguoi gui du lieu trong mot doi tuong duy nhat
class Item(BaseModel):
    name: str
    price: float

@app.post("/Embed_a_single_body_parameter/")
async def create_item(item: Item = Body(..., embed=True)):
    return {"item": item}

#-------Body-Fields----------
# Sử dụng Field để định nghĩa các trường trong body của yêu cầu HTTP, bao gồm các ràng buộc như độ dài tối đa, mô tả, v.v.
class Item(BaseModel):
    name: str = Field(..., title="Tên sản phẩm", max_length=50)
    description: str | None = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    tax: float | None = None

@app.post("/Body-Fields/")
async def create_item(item: Item):
    return item

#-------Body - Nested Models----------
# Sử dụng các mô hình lồng nhau (nested models) để định nghĩa cấu trúc dữ liệu phức tạp hơn trong body của yêu cầu HTTP
class User(BaseModel):
    username: str
    email: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = [] # co the su dung "set" de du lieu khong bi trung lap
    owner: User  # <--- đây là nested model

@app.put("/Body_Nested_Models/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

#-------Declare Request Example Data----------
# giup định nghĩa các ví dụ dữ liệu trong OpenAPI để người dùng có thể hiểu rõ hơn về cấu trúc dữ liệu mà API yêu cầu
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
# tu dong hieu khong can phai goi 
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


@app.put("/Declare_Request_Example_Data/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
# vi du Field additional arguments
# giup định nghĩa các trường trong body của yêu cầu HTTP với các tham số bổ sung như mô tả, ví dụ, v.v.
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/Field_additional_arguments/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

#-------Using the openapi_examples Parameter----------
# tao nhieu vi du minh hoa du lieu trong OpenAPI
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/Using the openapi_examples Parameter/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
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

#-------Extra Data Types----------
# giup sử dụng các kiểu dữ liệu bổ sung như datetime, time, timedelta, UUID, v.v. trong các tham số của API

@app.put("/Extra_Data_Types/{item_id}")
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
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }

#-------Cookie Parameters----------
@app.get("/Cookie_Parameters/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

#-------Response Model - Return Type----------

#Dùng response_model=Model để đảm bảo dữ liệu trả về có đúng cấu trúc mong muốn.

class Item(BaseModel):
    name: str
    price: float

@app.get("/response_model=Model/{item_id}", response_model=Item)
async def get_item(item_id: int):
    return {"name": "Bánh mì", "price": 15000}

#Dùng response_model_exclude để ẩn các trường không muốn trả về.
class Item(BaseModel):
    name: str
    price: float
    secret_code: str

@app.get("/response_model_exclude/{item_id}", response_model=Item, response_model_exclude={"secret_code"})
async def get_item(item_id: int):
    return {"name": "Bánh mì", "price": 15000, "secret_code": "ABC123"}

#Dùng response_model_include để chỉ trả về một số trường cụ thể.
class Item(BaseModel):
    name: str
    price: float
    secret_code: str
@app.get("/response_model_include/{item_id}", response_model=Item, response_model_include={"name"})
async def get_item(item_id: int):
    return {"name": "Bánh mì", "price": 15000, "secret_code": "ABC123"}

#Dùng response_model_exclude_unset để loại bỏ các trường không được thiết lập.
class Item(BaseModel):
    name: str
    price: float
    secret_code: str | None = None
@app.get("/response_model_exclude_unset/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_item(item_id: int):
    return {"name": "Bánh mì", "price": 15000}

#Dùng response_model_exclude_defaults để loại bỏ các trường có giá trị mặc định.
class Item(BaseModel):
    name: str
    price: float
    secret_code: str = "default_code"
@app.get("/response_model_exclude_defaults/{item_id}", response_model=Item, response_model_exclude_defaults=True)
async def get_item(item_id: int):
    return {"name": "Bánh mì", "price": 15000, "secret_code": "default_code"}
   
# ví dụ cách sử dụng kế thừa model trong FastAPI/Pydantic để tách dữ liệu nhạy cảm (password) khỏi dữ liệu trả về.
class UserIn(BaseModel):
    username: str
    password: str
    email: str  
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any: #-> Any kiểu trả về có thể là bất kỳ kiểu dữ liệu nào
    return user

#-------Extra Models----------
# Sử dụng Extra Models để định nghĩa các mô hình phức tạp hơn

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: str | None = None

# Giả lập hàm băm mật khẩu
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

# Giả lập hàm lưu người dùng vào cơ sở dữ liệu
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/Extra_Models_user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
#--------------- Reduce duplication-----------------
# Giảm thiểu sự trùng lặp mã bằng cách sử dụng các mô hình cơ sở (base models) và kế thừa
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/Reduce_duplication_user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

#-------Union or anyOf----------
# Sử dụng Union để cho phép nhiều kiểu dữ liệu khác nhau trong một trường
# Nếu dictionary trả về có "type": "car", FastAPI sẽ tự động ánh xạ (parse) thành kiểu CarItem.
# Nếu dictionary có "type": "plane" và bao gồm thêm trường "size", FastAPI sẽ ánh xạ thành kiểu PlaneItem.

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/Union_or_anyOf/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

#-------Response Status Code----------
# Sử dụng status_code để xác định mã trạng thái HTTP trả về

@app.post("/Response_Status_Code/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}

#-------Form Dada----------
# Sử dụng Form để nhận dữ liệu từ biểu mẫu HTML

@app.post("/form-data/")
async def create_item(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    tax: float | None = Form(None)
):
    return {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax
    }





# Trả về giao diện HTML Form để test
@app.get("/", response_class=HTMLResponse)
async def form_page():
    return """
    <form action="/login/" method="post">
        <input type="text" name="username" placeholder="Tên đăng nhập">
        <input type="password" name="password" placeholder="Mật khẩu">
        <button type="submit">Đăng nhập</button>
    </form>
    """

# Nhận dữ liệu từ form gửi đến
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}

#-------Form Models----------
# Sử dụng Pydantic để định nghĩa mô hình dữ liệu cho form
class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data


#-------Request Files----------
# Sử dụng File để nhận tệp tin từ yêu cầu HTTP
@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}

#-------Multiple Files----------
@app.post("/Multiple_files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/Multiple_uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

#-------File and Form Data----------
@app.post("/File_and_Form_Data/")
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

#-----------Handling Errors----------
# Ví dụ về cách xử lý lỗi trong FastAPI bằng cách sử dụng HTTPException
items = {"foo": "The Foo Wrestlers"}


@app.get("/Handling_Errors/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# vi du Add custom headers
items = {"foo": "The Foo Wrestlers"}


@app.get("/Add_custom_headers/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

# vi du Install custom exception handlers
#Đoạn mã này là ví dụ về xử lý ngoại lệ tùy chỉnh (custom exception handling) trong FastAPI bằng cách tạo một exception riêng (UnicornException) và gán một hàm xử lý (exception handler) cho nó.


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name



@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# vi du Override the default exception handlers
# giup ghi đè các trình xử lý ngoại lệ mặc định của FastAPI để tùy chỉnh cách xử lý các lỗi HTTP và lỗi xác thực yêu cầu
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

#vi du Use the RequestValidationError body
# giup trả về thông tin chi tiết về lỗi xác thực yêu cầu trong phần body của phản hồi
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item(BaseModel):
    title: str
    size: int


@app.post("/Use_the_RequestValidationError_body/")
async def create_item(item: Item):
    return item

#vi du Reuse FastAPI's exception handlers
# Ghi log nhưng vẫn dùng lỗi mặc định của FastAPI
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"📛 HTTP ERROR: {repr(exc)}")  # log
    return await http_exception_handler(request, exc)  # giữ lỗi mặc định

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"📛 VALIDATION ERROR: {exc}")  # log
    return await request_validation_exception_handler(request, exc)  # giữ lỗi mặc định

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Tôi không thích số 3.")
    return {"item_id": item_id}

#-------Path Operation Configuration----------
# vi du Response Status Code
# mac dinh FastAPI se tra ve 200 OK, neu muon tra ve ma trang thai khac ta co the su dung tham so status_code
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

# vi du Tags
# Tags giup phan loai cac API trong giao dien Swagger UI
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

# vi du Tags with Enum
# sử dụng Enum để định nghĩa các tag, giúp quản lý và sử dụng lại dễ dàng hơn
class Tags(Enum):
    items = "items"
    users = "users"


@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]
# vi du Summary and Description
# Sử dụng summary và description để mô tả ngắn gọn và chi tiết về API
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post(
    "/Create_items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item
# vi du Deprecate a path operation
# Đánh dấu một API là đã lỗi thời (deprecated) để người dùng biết rằng nó sẽ không còn được hỗ trợ trong tương lai

@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
#-------JSON Compatible Encoder----------
# Sử dụng jsonable_encoder để chuyển đổi dữ liệu thành định dạng JSON tương thích
# tranh việc lỗi khi trả về dữ liệu không phải là kiểu dữ liệu JSON hợp lệ
fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None



@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data

#-------Body - Updates----------
# Update replacing with PUT
#giup thay thế toàn bộ dữ liệu của một đối tượng
class Item(BaseModel):
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

## Sử dụng PUT để cập nhật toàn bộ dữ liệu của một đối tượng
@app.get("/Update_replacing_with_PUT/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/Update_replacing_with_PUT/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# Update partial with PATCH
#giup cập nhật một phần dữ liệu của một đối tượng mà không cần thay thế toàn bộ
class Item(BaseModel):
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


@app.get("/Update_partial_with_PATCH/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.patch("/Update_partial_with_PATCH/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    # Lấy dữ liệu đã lưu trữ từ items
    stored_item_data = items[item_id]
    # Chuyển đổi dữ liệu đã lưu trữ thành mô hình Item
    stored_item_model = Item(**stored_item_data)
    # Cập nhật dữ liệu từ item, chỉ những trường nào được cung cấp
    # exclude_unset=True sẽ loại bỏ các trường không được thiết lập trong item
    update_data = item.dict(exclude_unset=True)
    # Cập nhật mô hình đã lưu trữ với dữ liệu mới
    updated_item = stored_item_model.copy(update=update_data)
    # Chuyển đổi mô hình đã cập nhật thành định dạng JSON tương thích
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item

#-------Dependencies----------
# Sử dụng Depends để tạo các phụ thuộc (dependencies) cho các hàm xử lý yêu cầu
#giup tái sử dụng mã và quản lý các phụ thuộc một cách hiệu quả

# Ví dụ về sử dụng Depends để tạo các tham số chung cho nhiều API
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# su dung Annotated để kết hợp các tham số chung với Depends
@app.get("/Dependencies_items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/Dependencies_users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

#-------Dependencies with Classes----------
# Sử dụng lớp để định nghĩa các phụ thuộc phức tạp hơn
#giup quản lý các tham số phức tạp và tái sử dụng mã một cách hiệu quả
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/Dependencies_with_Classes_items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/Dependencies_with_Classes_users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
#--------Sub-dependencies----------
# Sử dụng phụ thuộc con (sub-dependencies) để tạo các phụ thuộc phức tạp hơn

# Ví dụ về phụ thuộc con để lấy các tham số chung
def query_extractor(q: str | None = None):
    return q

# Sử dụng phụ thuộc con trong một hàm xử lý yêu cầu
def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

# Sử dụng phụ thuộc con trong một hàm xử lý yêu cầu
@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}

#--------Dependencies in path operation decorators----------
# Sử dụng phụ thuộc trong các decorator của path operation
#giúp tái sử dụng mã và quản lý các phụ thuộc một cách hiệu quả

# Ví dụ về phụ thuộc để xác thực token
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# Ví dụ về phụ thuộc để xác thực khóa API
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# Sử dụng phụ thuộc trong các path operation
# giup xác thực token và khóa API trước khi xử lý yêu cầu
@app.get("/Dependencies_in_path_operation_decorators_items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

#--------Global Dependencies----------
# Sử dụng phụ thuộc toàn cục để áp dụng cho tất cả các path operation
# Ví dụ về phụ thuộc để xác thực token
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# Ví dụ về phụ thuộc để xác thực khóa API
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# Tạo ứng dụng FastAPI với các phụ thuộc toàn cục
##app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


# Sử dụng phụ thuộc trong các path operation
# giup xác thực token và khóa API trước khi xử lý yêu cầu
@app.get("/Global_Dependencies_items/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

#--------Dependencies with yield----------
# Sử dụng yield để tạo các phụ thuộc có thể dọn dẹp tài nguyên sau khi sử dụng
# Dependency dùng yield
# trong FastAPI cho phép bạn tạo các phụ thuộc có thể dọn dẹp tài nguyên sau khi sử dụng, ví dụ như đóng kết nối cơ sở dữ liệu hoặc giải phóng tài nguyên khác.
def get_db():
    db = "FakeDatabaseConnection()"  # Setup
    try:
        yield db  # Sử dụng trong route
    finally:
        print("Đóng kết nối DB")  # Cleanup

@app.get("/Dependencies_with_yield_items/")
def read_items(db: str = Depends(get_db)):
    print(f"Dùng DB: {db}")
    return {"message": "Lấy dữ liệu từ DB"}

#--------Middleware----------
# Sử dụng middleware để xử lý các yêu cầu và phản hồi trước khi chúng được gửi đến hoặc nhận từ client
# vi dụ về middleware để ghi log các yêu cầu
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"Yêu cầu: {request.method} {request.url}")
        response: Response = await call_next(request)
        print(f"Phản hồi: {response.status_code}")
        return response
# su dung thi bo #
#app = FastAPI()
#app.add_middleware(LoggingMiddleware)
@app.get("/Middleware_items/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]



#--------CORS (Cross-Origin Resource Sharing)----------
# Sử dụng CORS để cho phép các yêu cầu từ các nguồn khác nhau
# Danh sách các origin được phép gọi đến backend
origins = [
    "http://localhost:3000",  # cho phép frontend local
    "https://yourdomain.com",  # cho phép domain thật
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # cho phép các domain này
    allow_credentials=True,
    allow_methods=["*"],  # cho phép tất cả phương thức (GET, POST,...)
    allow_headers=["*"],  # cho phép tất cả header
)

@app.get("/CORS_items/")
async def read_items():
    return [{"item": "A"}, {"item": "B"}]

