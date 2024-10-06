from typing import Iterable

from lecture_2.hw.shop_api.contracts import ItemPatchRequest
from lecture_2.hw.store.resources import Cart, Item, ItemInfo

_cart_data = dict[int, Cart]()
_item_data = dict[int, Item]()


def _int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_item_id_generator = _int_id_generator()
_cart_id_generator = _int_id_generator()


def add_item(item_info: ItemInfo) -> Item:
    item_id = next(_item_id_generator)
    _item_data[item_id] = Item(item_id, item_info)
    return _item_data[item_id]


def get_item(item_id: int) -> Item | None:
    return _item_data[item_id]


def get_items(offset: int = 0, limit: int = 10, min_price: float = .0, max_price: float | None = None,
              show_deleted: bool = False) -> list[Item]:
    if max_price is None:
        max_price = float('inf')
    item_id = offset
    result = list[Item]()
    while item_id in _item_data and len(result) < limit:
        item = _item_data[item_id]
        if min_price < item.item_info.price < max_price and (
                not show_deleted and not item.item_info.deleted or show_deleted):
            result.append(item)
        item_id += 1
    return result


def put_item(item_id: int, item_info: ItemInfo) -> Item | None:
    if item_id in _item_data:
        _item_data[item_id] = Item(item_id, item_info)
        return _item_data[item_id]
    return None


def patch_item(item_id: int, patch_request: ItemPatchRequest) -> Item | None:
    if item_id in _item_data and not _item_data[item_id].item_info.deleted:
        if patch_request.name is not None:
            _item_data[item_id].item_info.name = patch_request.name
        if patch_request.price is not None:
            _item_data[item_id].item_info.price = patch_request.price
        return _item_data[item_id]
    return None


def delete_item(item_id: int) -> bool:
    if item_id in _item_data:
        _item_data[item_id].item_info.deleted = True
        return True
    return False


def post_cart() -> Cart:
    cart_id = next(_cart_id_generator)
    _cart_data[cart_id] = Cart(cart_id, list())
    return _cart_data[cart_id]


def get_cart(cart_id: int) -> Cart | None:
    return _cart_data.get(cart_id)


def get_carts(offset: int = 0, limit: int = 10, min_price: float = .0, max_price: float | None = None,
              min_quantity: int = 0, max_quantity: int | None = None) -> list[Cart]:
    if max_price is None:
        max_price = float('inf')
    if max_quantity is None:
        max_quantity = float('inf')
    cart_id = offset
    result = list[Cart]()
    while cart_id in _cart_data and len(result) < limit:
        cart = _cart_data[cart_id]
        if min_price < cart.price < max_price and min_quantity < cart.quantity < max_quantity:
            result.append(cart)
        cart_id += 1
    return result


def add_item_to_cart(cart_id: int, item_id: int) -> bool:
    if item_id in _item_data and cart_id in _cart_data:
        item = _item_data.get(item_id)
        _cart_data[cart_id].add_item(item)
        return True
    return False
