from typing import Optional, List
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select

# ---------- Định nghĩa model ----------
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None
    power: Optional[str] = None

# ---------- Kết nối DB ----------
sqlite_file_name = "heroes.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)

# ---------- Tạo bảng ----------
def create_db():
    SQLModel.metadata.create_all(engine)

# ---------- Tạo app ----------
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is from database.py"}

@app.on_event("startup")
def on_startup():
    create_db()

# ---------- API ----------

@app.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/", response_model=List[Hero])

def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}
