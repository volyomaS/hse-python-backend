from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Response, HTTPException, Query
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from store_backend.shop_api.contracts import CartResponse, ItemResponse, ItemPatchRequest
from store_backend.store import queries
from store_backend.store.resources import ItemInfo

router = APIRouter()


@router.post(
    "/item",
    status_code=HTTPStatus.CREATED
)
async def post_item(info: ItemInfo, response: Response) -> ItemResponse:
    item = queries.add_item(info)

    response.headers["location"] = f"/item/{item.id}"

    return ItemResponse.from_item(item)


@router.get(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully got item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to get the item with this id",
        },
    }
)
async def get_item(id: int) -> ItemResponse:
    item = queries.get_item(id)

    if item is None or item.item_info.deleted:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )

    return ItemResponse.from_item(item)


@router.get(
    "/item"
)
async def get_all_items(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[NonNegativeFloat, Query()] = .0,
        max_price: Annotated[NonNegativeFloat | None, Query()] = None,
        show_deleted: Annotated[bool, Query()] = False
) -> list[ItemResponse]:
    return [ItemResponse.from_item(item) for item in
            queries.get_items(offset, limit, min_price, max_price, show_deleted)]


@router.put(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully replaced",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to replace, not found",
        },
    }
)
async def replace_item(id: int, info: ItemInfo) -> ItemResponse:
    item = queries.put_item(id, info)
    if item is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Failed to replace, not found /item/{id}",
        )
    return ItemResponse.from_item(item)


@router.patch(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully replaced",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to change, not found",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to change, incorrect patch request",
        },
    }
)
async def change_item(id: int, patch_request: ItemPatchRequest) -> ItemResponse:
    if patch_request.deleted:
        raise HTTPException(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "Failed to change, incorrect patch request, can't modify deleted",
        )

    item = queries.patch_item(id, patch_request)

    if item is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Failed to change, not found /item/{id}",
        )

    return ItemResponse.from_item(item)


@router.delete(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully deleted",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to delete, not found",
        },
    }
)
async def delete_item(id: int) -> Response:
    if queries.delete_item(id):
        return Response('')
    raise HTTPException(
        HTTPStatus.NOT_FOUND,
        f"Failed to delete, not found /item/{id}",
    )


@router.post(
    "/cart",
    status_code=HTTPStatus.CREATED
)
async def create_cart(response: Response) -> CartResponse:
    cart = queries.post_cart()
    response.headers["location"] = f"/item/{cart.id}"
    return CartResponse.from_cart(cart)


@router.get(
    "/cart/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully got cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to get the cart with this id",
        },
    }
)
async def get_cart(id: int) -> CartResponse:
    cart = queries.get_cart(id)

    if cart is None:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /cart/{id} was not found",
        )

    return CartResponse.from_cart(cart)


@router.get(
    "/cart"
)
async def get_all_carts(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[NonNegativeFloat, Query()] = .0,
        max_price: Annotated[NonNegativeFloat | None, Query()] = None,
        min_quantity: Annotated[NonNegativeInt, Query()] = 0,
        max_quantity: Annotated[NonNegativeInt | None, Query()] = None
) -> list[CartResponse]:
    return [CartResponse.from_cart(cart) for cart in
            queries.get_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)]


@router.post(
    "/cart/{cart_id}/add/{item_id}"
)
async def add_item_to_cart(cart_id: int, item_id: int):
    queries.add_item_to_cart(cart_id, item_id)
