from datetime import date
from typing import Optional

from src.allocation.domain import model
from src.allocation.domain.model import Batch, OrderLine
from src.allocation.adapters.repository import AbstractRepository
from src.allocation.service_layer import unit_of_work


class InvalidSku(Exception):
    pass


def add_batch(
    ref: str,
    sku: str,
    qty: int,
    eta: Optional[date],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    orderid: str,
    sku: str,
    qty: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
    return batchref


# def deallocate(orderid: str, sku: str, qty: int, uow: unit_of_work.AbstractUnitOfWork) -> str:
#     line = OrderLine(orderid, sku, qty)
#     batches = repo.list()
#     if not is_valid_sku(line.sku, batches):
#         raise InvalidSku(f"Invalid sku {sku}")
#     batchref = model.deallocate(line, batches)
#     session.commit()
#     return batchref
