from settings import db
from logic.additional import print_order, get_actual_cost


def snipe(min_price=1000, max_price=2000000, min_cashup=100000):
    # getting bid orders that will end soon and going throw them all in loop
    for bid_order in db.get_orders_by_keys(type_='bid', min_time=0.5, max_time=10):
        # getting prices of the bin orders that has the same short name and tier as a bid order
        cost_data = db.get_orders_by_keys(name=bid_order.get('short_name'),
                                          is_full_name=False,
                                          tier=bid_order.get('tier'),
                                          row='starting_bid',
                                          type_='bin',
                                          min_start_bid=min_price,
                                          max_start_bid=max_price)

        # do nothing if got 0 bin orders by request
        if len(cost_data) == 0:
            continue

        min_bin = min(cost_data)    # the minimum cost of this order
        cashup = min_bin - get_actual_cost(bid_order)    # difference between bin order cost and bid order cost

        if cashup > min_cashup:
            print_order(bid_order, additional=f'\nMin bin: {min_bin}$\nCashup: {cashup}$')


def by_name(name='Null', is_full_name='n'):
    """find orders by name or short name"""

    # if is_full_name not in 'yYnN' so we cant know short or full name was given
    if is_full_name not in 'yYnN':
        raise ValueError(f'There only 2 statuses yY/nN, got ~~> {is_full_name}')

    is_full_name = is_full_name == 'y'   # converting string to bool, yY = True, nN = False
    for order in db.get_orders_by_keys(name=name, is_full_name=is_full_name):
        print_order(order)


def count_orders():
    """print the count of all orders in db"""
    print(f'There {len(db.get_orders_by_keys(row="end"))} orders in db')
