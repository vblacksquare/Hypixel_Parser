from sqlite3 import connect
from logic.additional import convert_order_type, clear_name, get_future_time, filters


class DbHandler:
    """class to handle sql requests. It can upload some data to db, get orders from db"""

    def __init__(self):
        self.__connection = connect('db/orders.db')  # connecting project db
        self.__cursor = self.__connection.cursor()  # creating cursor to proceed sql requests
        self.__table_name = 'orders'  # orders table where all hypixel orders must be

    def upload_order_to_db(self, order):
        """
        upload hypixel order to d (actually it isn`t saving them into real db.
        To save them into real db you need to use function self.save()))
        """

        # do nothing if item in the trash list
        """if order.get('item_name') in filters['trash']:
            return"""

        # converting dictionary to tuple
        data = order.get('item_name'), clear_name(order.get('item_name')), \
            order.get('tier'), order.get('extra'), order.get('end'), \
            order.get('starting_bid'), order.get('highest_bid_amount'), \
            int(not order.get('bin') is None)

        # sql request
        self.__cursor.execute(f"INSERT INTO {self.__table_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)

    def get_orders_by_keys(self, name=None, is_full_name=False, tier=None, row='*',
                           type_=None, max_time=None, min_time=None, min_start_bid=None, max_start_bid=None,
                           min_highest_bid=None, max_highest_bid=None):
        """returning tuple of orders information or order dictionary by keys"""

        sql = f'SELECT {row} FROM {self.__table_name}'  # base sql request

        # checking for given keys: if key is not None, key will be in final sql request else not
        name = '' if name is None else ''.join(('name' if is_full_name else 'short_name',
                                                '="', name.replace("'", ''), '"'))
        tier = '' if tier is None else f"tier='{tier}'"
        type_ = '' if type_ is None else f"is_bin={convert_order_type(type_)}"
        time = '' if min_time is None or max_time is None else \
            f'end BETWEEN {get_future_time(min_time)} AND {get_future_time(max_time)}'
        starting_bid = '' if min_start_bid is None or max_start_bid is None else \
            f'starting_bid BETWEEN {min_start_bid} AND {max_start_bid}'
        highest_bid = '' if min_highest_bid is None or max_highest_bid is None else \
            f'highest_bid BETWEEN {min_highest_bid} AND {max_highest_bid}'

        # constructing sql order with given keys
        has_used_where = False  # needs to use only one time "WHERE" in sql request
        for part in (name, tier, type_, time, starting_bid, highest_bid):
            # check if key is not empty
            if part == '':
                continue
            if not has_used_where:
                sql += f' WHERE {part}'
                has_used_where = True
            else:
                sql += f' AND {part}'

        # getting data from sql request
        data = self.__cursor.execute(sql)

        # if argument row is empty (actually it must equal "*") return data like a list of dictionaries
        # else return list of variables
        keys = ('name', 'short_name', 'tier', 'extra', 'end', 'starting_bid', 'highest_bid', 'type')
        return [x[0] for x in data] if row != '*' else \
            [{keys[x]: tuple_[x] if not x == 7 else convert_order_type(tuple_[x]) for x in range(8)} for tuple_ in data]

    def save(self):
        """saving uploaded data into db"""
        self.__connection.commit()

    def clear_orders(self):
        """clearing orders in temp db, also need to save to delete from real db"""
        self.__cursor.execute(f"DELETE FROM {self.__table_name};")

    def delete_table(self):
        """deleting table in db, isn`t need to save db"""
        self.__cursor.execute(f"DROP TABLE {self.__table_name}")

    def create_table(self):
        """creating table in db"""
        self.__cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.__table_name}
            (name text, short_name text, tier text, extra text, end integer, 
            starting_bid integer, highest_bid integer, is_bin integer)"""
        )
