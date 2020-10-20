"""

Features and Test Planning
A clothing and footwear store would like to move management of their items from paper to a new computer the owner bought.
While the owner would like many features, she's content with software that could perform the following upcoming tasks immediately.

Record the 10 new Nike sneakers that she recently bought. Each is worth $50.00.
Add 5 more Adidas sweatpants that cost $70.00 each.
She's expecting a customer to buy 2 of the Nike sneakers
She's expecting another customer to buy 1 of the sweatpants.

We can use these requirements to create our first integration test. Before we get to writing it,
let's flesh out the smaller components a bit to figure out what would be our inputs and output,
function signatures and other system design elements.

Each item of stock will have a name, price and quantity. We'll be able to add new items,
add stock to existing items and of course remove stock.

When we instantiate an Inventory object, we'll want the user to provide a limit. The limit will
have a default value of 100. Our first test would be to check the limit when instantiating an object.
To ensure that we don't go over our limit, we'll need to keep track of the total_items counter.
When initialized, this should be 0.

We'll need to add 10 Nike sneakers and the 5 Adidas sweatpants to the system. We can create an add_new_stock()
method that accepts a name, price, and quantity.

We should test that we can add an item to our inventory object. We should not be able to add an item with a negative
quantity, the method should raise an exception. We also should not be able to add any more items if we're at the our

limit, that should also raise an exception.
Customers will be buying these items soon after entry, so we'll need a remove_stock() method as well.
This function would need the name of the stock and the quantity of items being removed. If the quantity being removed
is negative or if it makes the total quantity for the stock below 0, then the method should raise an exception.
Additionally, if the name provided is not found in our inventory, the method should raise an exception.

"""
import pytest

from tdd_playground.inventory.inventory import Inventory, InvalidQuantityException, NoSpaceException, \
    ItemNotFoundException


@pytest.fixture
def no_stock_inventory():
    """Returns an empty inventory that can store 10 items"""
    return Inventory(limit=10)


# ...
# Add a new fixture that contains stocks by default
# This makes writing tests easier for our remove function
@pytest.fixture
def ten_stock_inventory():
    """Returns an inventory with some test stock items"""
    inventory = Inventory(limit=20)
    inventory.add_new_stock('Puma Test', 100.00, 8)
    inventory.add_new_stock('Rebook Test', 25.00, 2)
    return inventory


def test_buy_and_sell_nikes_adidas():
    # Create inventory object
    inventory = Inventory()
    assert inventory.limit == 100
    assert inventory.total_items == 0

    # Add the new nike sneakers
    inventory.add_new_stock('Nike Sneakers', 50.00, 10)
    assert inventory.total_items == 10

    # Add the new adidas sweatpants
    inventory.add_new_stock('Adidas Sweatpants', 70.00, 5)
    assert inventory.total_items == 15

    # Remove 2 sneakers to sell to the first customer
    inventory.remove_stock('Nike Sneakers', 2)
    assert inventory.total_items == 13

    # Remove 1 sweatpants to sell to the next customer
    inventory.remove_stock('Adidas Sweatpants', 1)
    assert inventory.total_items == 12


def test_default_inventory():
    # Test that the default limit is 100
    inventory = Inventory()
    assert inventory.limit == 100
    assert inventory.total_items == 0


def test_custom_inventory_limit():
    # Test that we can set a custom limit
    inventory = Inventory(limit=25)
    assert inventory.limit == 25
    assert inventory.total_items == 0


"""Refactor using this test on test_add_new_stock"""


# def test_add_new_stock_success(no_stock_inventory):
#     no_stock_inventory.add_new_stock('Test Jacket', 10.00, 5)
#     assert no_stock_inventory.total_items == 5
#     assert no_stock_inventory.stocks['Test Jacket']['price'] == 10.00
#     assert no_stock_inventory.stocks['Test Jacket']['quantity'] == 5


# Refactor using this test on test_add_new_stock"""

# @pytest.mark.parametrize('name, price, quantity, exception',[
#     ('Test Jacket', 10.00, 0, InvalidQuantityException('Cannot add a quantity of 0. All new stocks must have at least '
#                                                        '1 item')),
#     ('Test Jacket', 10.00, 25, NoSpaceException('Cannot add these 25 items. Only 10 more items can be stored'))])
# def test_add_new_stock_bad_input(name, price, quantity, exception):
#     inventory = Inventory(10)
#
#     try:
#         inventory.add_new_stock(name=name, price=price, quantity=quantity)
#     except (InvalidQuantityException, NoSpaceException) as inst:
#         """First ensure the exception is of the right type"""
#         assert isinstance(inst, type(exception))
#
#         """Ensure that exceptions have the same message"""
#         assert inst.args == exception.args
#     else:
#         pytest.fail("Expected error but found none")


@pytest.mark.parametrize('name,price,quantity,exception', [
    ('Test Jacket', 10.00, 0, InvalidQuantityException(
        'Cannot add a quantity of 0. All new stocks must have at least 1 item')),
    ('Test Jacket', 10.00, 25, NoSpaceException(
        'Cannot add these 25 items. Only 10 more items can be stored')),
    ('Test Jacket', 10.00, 5, None)
])
def test_add_new_stock(no_stock_inventory, name, price, quantity, exception):
    try:
        no_stock_inventory.add_new_stock(name=name, price=price, quantity=quantity)

    except (InvalidQuantityException, NoSpaceException) as inst:
        """First ensure the exception is of the right type"""
        assert isinstance(inst, type(exception))

        """Ensure that exceptions have the same message"""
        assert inst.args == exception.args

    else:
        assert no_stock_inventory.total_items == quantity
        assert no_stock_inventory.stocks[name]['price'] == price
        assert no_stock_inventory.stocks[name]['quantity'] == quantity


# ...
# Note the extra parameters, we need to set our expectation of
# what totals should be after our remove action
@pytest.mark.parametrize('name, quantity, exception, new_quantity, new_total',[
    ('Puma Test', 0,
     InvalidQuantityException(
        'Cannot remove a quantity of 0. Must remove at least 1 item'),
     0, 0),
    ('Not Here', 5,
     ItemNotFoundException(
         'Could not find Not Here in our stocks. Cannot remove non-existing stock'),
        0, 0),
    ('Puma Test', 25,
     InvalidQuantityException(
        'Cannot remove these 25 items. Only 8 items are in stock'),
     0, 0),
    ('Puma Test', 5, None, 3, 5)
])
def test_remove_stock(ten_stock_inventory, name, quantity, exception, new_quantity, new_total):
    try:
        ten_stock_inventory.remove_stock(name, quantity)

    except (InvalidQuantityException, NoSpaceException, ItemNotFoundException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert ten_stock_inventory.stocks[name]['quantity'] == new_quantity
        assert ten_stock_inventory.total_items == new_total