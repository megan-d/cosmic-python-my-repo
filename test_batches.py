from datetime import date
from model import Batch, OrderLine


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_to_batch_if_available_is_greater_than_required():
    pass


def test_can_allocate_to_batch_if_available_is_equal_to_required():
    pass


def test_cannot_allocate_to_batch_if_available_is_less_than_required():
    pass


def test_allocation_is_idempotent():
    pass
