import sqlalchemy as sa
from fastapi import APIRouter, Depends

from app.database import SessionDep
from models import Cart, Item
from models.checkout import Checkout
from models.receipt import Receipt
from utils.Oauth2_schema import oauth2_scheme

checkout_router = APIRouter()


@checkout_router.post("", response_model=int)
async def create_checkout(
    session: SessionDep,
    token: dict = Depends(oauth2_scheme),
):
    user_id = int(token["sub"])

    q = (
        sa.select(Cart.item_id, Cart.amount, Item.price)
        .select_from(sa.outerjoin(Cart, Item, Cart.item_id == Item.id))
        .where(Cart.user_id == user_id)
    )
    cart_values = (await session.execute(q)).mappings().fetchall()

    total_price = sum(i["price"] * i["amount"] for i in cart_values)

    q = sa.insert(Receipt).values({Receipt.user_id: user_id, Receipt.price: total_price}).returning(Receipt.id)

    receipt_id = (await session.execute(q)).scalar()

    q = sa.insert(Checkout).values(
        [
            {
                Checkout.reciept_id: receipt_id,
                Checkout.item_id: a["item_id"],
                Checkout.amount: a["amount"],
                Checkout.price: a["price"],
            }
            for a in cart_values
        ]
    )
    await session.execute(q)

    return receipt_id

@checkout_router.get("/receipt/{receipt_id}", response_model=Receipt)