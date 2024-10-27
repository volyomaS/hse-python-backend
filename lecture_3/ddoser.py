import json
from random import randint, random

import requests


def create_items() -> list[int]:
    ids = []
    for _ in range(500):
        rand_id = randint(0, 100000)
        response = requests.post(
            "http://localhost:8080/item",
            json={
                "name": f"item{rand_id}",
                "price": random(),
            },
        )
        ids.append(json.loads(response.text)['id'])
        print(response.status_code, response.text)
    return ids


def get_items_exists(ids: list[int]):
    for rand_id in ids:
        response = requests.get(
            f"http://localhost:8080/item/{rand_id}"
        )
        print(response.status_code, response.text)


def get_items_non_exists(ids: list[int]):
    max_id = max(ids)
    for rand_id in range(max_id, max_id + 500):
        response = requests.get(
            f"http://localhost:8080/item/{rand_id}"
        )
        print(response.status_code, response.text)


if __name__ == '__main__':
    rand_ids = create_items()
    get_items_exists(rand_ids)
    get_items_non_exists(rand_ids)
