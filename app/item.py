import sqlalchemy as sa
from fastapi import APIRouter, HTTPException, Body
from starlette import status

from app.database import SessionDep
from models.item import Item
from schemas.item_scheme import CreateItemSchema, ItemSchema, UpdateItemSchema

item_router = APIRouter()


@item_router.post("", response_model=int)
async def item_add(session: SessionDep, item_data: CreateItemSchema):
    q = (
        sa.insert(Item)
        .values(
            {
                Item.name: item_data.name,
                Item.description: item_data.description,
                Item.price: item_data.price,
            }
        )
        .returning(Item.id)
    )
    # item_id = (await session.execute(q)).mappings().fetchall()
    # item_id = (await session.execute(q)).mappings().fetchone()
    item_id = (await session.execute(q)).scalar()
    return item_id


@item_router.delete("/{item_id}", response_model=int)
async def item_delete(item_id: int, session: SessionDep):
    q = sa.delete(Item).where(Item.id == item_id).returning(Item.id)
    item_id = (await session.execute(q)).scalar()
    if item_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    return item_id


@item_router.post("/{item_id}")
async def item_update(
    item_id: int, session: SessionDep, item_data: UpdateItemSchema = Body(...)
):
    q = (
        sa.update(Item)
        .where(Item.id == item_id)
        .values(**item_data.model_dump(exclude_unset=True))
        .returning(Item.id, Item.name, Item.description)
    )

    response = (await session.execute(q)).mappings().fetchone()

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    return response


@item_router.get("/{item_id}", response_model=ItemSchema)
async def item_read(item_id: int, session: SessionDep):
    q = sa.select(Item.name, Item.description, Item.id).where(Item.id == item_id)

    response = (await session.execute(q)).mappings().fetchone()
    return response


@item_router.get("", response_model=list[ItemSchema])
async def show_item_list(session: SessionDep):
    q = sa.select(Item.name, Item.description, Item.id, Item.price)
    response = (await session.execute(q)).mappings().all()
    return response
