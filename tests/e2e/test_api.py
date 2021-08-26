import pytest
import uuid
import pytest
import requests

from allocation import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    sku, other_sku = random_sku(), random_sku(name="other")
    earlybatch = random_batchref(name=1)
    laterbatch = random_batchref(name=2)
    otherbatch = random_batchref(name=3)
    add_stock([

    ])
