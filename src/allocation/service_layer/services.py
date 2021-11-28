from datetime import date
from typing import Optional

from src.allocation.domain import model
from src.allocation.domain.model import Batch, OrderLine
from src.allocation.adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session) -> None:
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()


def allocate(orderid: str, sku: str, qty: int, uow: unit_of_work.AbstractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def deallocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session) -> str:
    line = OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {sku}")
    batchref = model.deallocate(line, batches)
    session.commit()
    return batchref
