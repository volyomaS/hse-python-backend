from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ItemInfo:
    name: str
    price: float
    deleted: bool = False


@dataclass(slots=True)
class Item:
    id: int
    item_info: ItemInfo

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.item_info.name,
            "price": self.item_info.price,
            "deleted": self.item_info.deleted
        }


@dataclass(slots=True)
class CartItem:
    item: Item
    quantity: int = 1

    @property
    def available(self):
        return not self.item.item_info.deleted

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.item.id,
            "name": self.item.item_info.name,
            "quantity": self.quantity,
            "available": self.available
        }


@dataclass(slots=True)
class Cart:
    id: int
    items: list[CartItem]

    @property
    def price(self):
        return sum((x.item.item_info.price * x.quantity for x in self.items))

    @property
    def quantity(self):
        return sum((x.quantity for x in self.items))

    def add_item(self, item: Item) -> bool:
        for cart_item in self.items:
            if cart_item.item.id == item.id:
                cart_item.quantity += 1
                return False
        self.items.append(CartItem(item))
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "items": self.items,
            "price": self.price
        }
