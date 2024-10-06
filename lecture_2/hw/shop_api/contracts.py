from typing import Any

from pydantic import BaseModel, ConfigDict

from lecture_2.hw.store.resources import Item, Cart, ItemInfo


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool

    @staticmethod
    def from_item(entity: Item):
        return ItemResponse(
            id=entity.id,
            name=entity.item_info.name,
            price=entity.item_info.price,
            deleted=entity.item_info.deleted
        )


class CartResponse(BaseModel):
    id: int
    items: list[dict[str, Any]]
    price: float
    quantity: int

    @staticmethod
    def from_cart(entity: Cart):
        return CartResponse(
            id=entity.id,
            items=[cart_item.to_dict() for cart_item in entity.items],
            price=entity.price,
            quantity=entity.quantity
        )

class ItemPatchRequest(BaseModel):
    name: str | None = None
    price: float | None = None
    deleted: bool | None = None

    model_config = ConfigDict(extra="forbid")

    def as_item_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=self.price, deleted=self.deleted)
