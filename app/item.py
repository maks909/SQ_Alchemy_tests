import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Body
from starlette import status

from app.database import SessionDep
from models import item
from schemas.item_scheme import CreateitemSchema, itemSchema, UpdateitemSchema

item_router = APIRouter()


@item_router.post("", response_model=int)
async def item_add(session: SessionDep, item_data: CreateitemSchema):
    q = (
        sa.insert(item)
        .values(
            {
                item.name: item_data.name,
                item.description: item_data.description,
                item.price: item_data.price,
            }
        )
        .returning(item.id)
    )
    # item_id = (await session.execute(q)).mappings().fetchall()
    # item_id = (await session.execute(q)).mappings().fetchone()
    item_id = (await session.execute(q)).scalar()
    return item_id


@item_router.delete("/{item_id}", response_model=int)
async def item_delete(item_id: int, session: SessionDep):
    q = sa.delete(item).where(item.id == item_id).returning(item.id)
    item_id = (await session.execute(q)).scalar()
    if item_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    return item_id


@item_router.post("/{item_id}")
async def item_update(item_id: int, session: SessionDep, item_data: UpdateitemSchema=Body(...)):
    q = (
        sa.update(item)
        .where(item.id == item_id)
        .values(**item_data.model_dump(exclude_unset=True))
        .returning(item.id, item.name, item.email)
    )

    response = (await session.execute(q)).mappings().fetchone()

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    return response


@item_router.get("/{item_id}", response_model=itemSchema)
async def item_read(item_id: int, session: SessionDep):
    q = sa.select(item.name, item.description, item.id).where(item.id == item_id)

    response = (await session.execute(q)).mappings().fetchone()
    return response
