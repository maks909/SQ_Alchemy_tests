import sqlalchemy as sa
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from app.database import SessionDep
from models import Cart
from schemas.cart_schema import CartSchema
from utils.Oauth2_schema import oauth2_scheme

cart_router = APIRouter()


@cart_router.get("/current", response_model=list[CartSchema])
async def cart_read(session: SessionDep, token: dict = Depends(oauth2_scheme)):
    user_id = int(token["sub"])
    q = sa.select(Cart.item_id, Cart.amount).where(Cart.user_id == user_id)
    cart = (await session.execute(q)).mappings().fetchall()
    return cart


@cart_router.post("/add")
async def cart_add(
    session: SessionDep,
    item_id: int = Body(..., embed=True),
    amount: int = Body(1, embed=True, gt=0),
    token: dict = Depends(oauth2_scheme),
):
    user_id = int(token["sub"])
    # q=sa.select(Cart).where(Cart.item_id == item_id).where(Cart.user_id == user_id)
    q = sa.select(Cart.id).where(
        sa.and_(Cart.item_id == item_id, Cart.user_id == user_id)
    )
    item = (await session.execute(q)).scalar()
    if item is None:
        q = sa.insert(Cart).values(
            {Cart.user_id: user_id, Cart.item_id: item_id, Cart.amount: amount}
        )
        await session.execute(q)
    else:
        q = (
            sa.update(Cart)
            .where(sa.and_(Cart.item_id == item_id, Cart.user_id == user_id))
            .values({Cart.amount: Cart.amount + amount})
        )
        await session.execute(q)


@cart_router.delete("/{item_id}")
async def cart_delete(
    session: SessionDep,
    item_id: int,
    token: dict = Depends(oauth2_scheme),
):
    user_id = int(token["sub"])
    q = (
        sa.delete(Cart)
        .where(sa.and_(Cart.item_id == item_id, Cart.user_id == user_id))
        .returning(Cart.id)
    )
    deleted_id = (await session.execute(q)).scalar()
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not deleted"
        )


@cart_router.post("/update")
async def cart_update(
    session: SessionDep,
    item_id: int = Body(..., embed=True),
    amount: int = Body(1, embed=True, gt=1),
    token: dict = Depends(oauth2_scheme),
):
    user_id = int(token["sub"])
    # q=sa.select(Cart).where(Cart.item_id == item_id).where(Cart.user_id == user_id)
    q = sa.select(Cart.id).where(
        sa.and_(Cart.item_id == item_id, Cart.user_id == user_id)
    )
    item = (await session.execute(q)).scalar()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    else:
        q = (
            sa.update(Cart)
            .where(sa.and_(Cart.item_id == item_id, Cart.user_id == user_id))
            .values({Cart.amount: amount})
        )
        await session.execute(q)
