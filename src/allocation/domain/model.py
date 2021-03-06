from datetime import date
from dataclasses import dataclass
from typing import Optional, List, Set


class OutOfStock(Exception):
    pass


# OrderLine is a value object - a domain object that is uniquely identified by the data it holds (rather than unique id)
@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        # batch keeps track of set of allocated OrderLine objects
        # when we allocate an OrderLine to a batch (if enough available quantity), we add to the set
        self._allocations = set()  # type: Set[OrderLine]

    # magic method that defines behavior of class for the == operator when comparing
    # this means that it's only looking at the reference
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    # magic method used to control behavior of objects when you add them to sets or use them as dict keys
    def __hash__(self):
        return hash(self.reference)

    # magic method for greater than
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        # allocated quantity is the sum of all OrderLine quantities in the allocations set
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {line.sku}")
