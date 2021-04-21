from datetime import datetime
from sys import stdout


def get_real_time():
    """return data like real time like a stamp"""
    return datetime.timestamp(datetime.now()) * 1000


def get_future_time(time, input_type='minute'):
    """return real time stamp + argument time"""
    return get_real_time() + time * time_formats[input_type] * 1000


def get_delta_time(order, out_type='minute'):
    """return time difference of real time and given order['end']"""
    difference = order.get('end') - get_real_time()
    unix = difference / 1000
    return round(unix / time_formats[out_type], 1)


def convert_order_type(type_):
    """bin = 1, bid = 0"""
    if isinstance(type_, str):
        input_, output = ('bin', 'bid'), (1, 0)
    elif isinstance(type_, int):
        output, input_ = ('bin', 'bid'), (1, 0)
    else:
        raise TypeError(f'There are only 2 types of input int/str, not {type(type_)}')
    if type_ == input_[0]:
        return output[0]
    elif type_ == input_[1]:
        return output[1]
    else:
        raise ValueError(f'There only 2 types of input types {input_}, got {type_}')


def clear_name(item_name):
    """removing item prefix and some bad chars like ✪, ✦, ⚚"""
    found = True
    while found:
        found = False
        for bad_word in filters['words']:
            if bad_word in item_name:
                item_name = item_name.replace(bad_word, '')
                found = True
    first_word = item_name.split()[0] if len(item_name.split()[0]) != 1 else item_name.split()[1]
    if first_word in filters['prefix']:
        return item_name.replace(first_word, '').strip()
    return item_name.strip()


def sort_by_key(arr, dict_key=None, print_count=True):
    """sorting orders by it keys"""
    def binary_search(start, end):
        if start == end:
            start_val = arr[start] if dict_key is None else arr[start]['end']
            if start_val > val:
                return start
            else:
                return start + 1

        if start > end:
            return start

        mid = (start + end) // 2
        middle = arr[mid] if dict_key is None else arr[mid][dict_key]
        if middle < val:
            return binary_search(mid + 1, end)
        elif middle > val:
            return binary_search(start, mid - 1)
        else:
            return mid

    count = 0
    for i in range(1, len(arr)):
        if print_count:
            count += 1
            stdout.write(f'\rSorting {count}/{len(arr)}')
        item = arr[i]
        val = item if dict_key is None else item[dict_key]
        j = binary_search(0, i - 1)
        arr = arr[:j] + [item] + arr[j:i] + arr[i + 1:]
    print()
    return arr


def get_actual_cost(order):
    """return the highest cost of an order"""
    return order['starting_bid'] if order['highest_bid'] == 0 else order['highest_bid']


def print_order(order, additional=''):
    """printing the order data"""
    print('-'*40,
          f"\nName: {order.get('name')}"
          f"\nShort name: {order.get('short_name')}"
          f"\nTier: {order.get('tier')}"
          f"\nType: {order.get('type')}"
          f"\nOrder ends in {get_delta_time(order)} minutes"
          f"\nStarting bid: {order.get('starting_bid')}$"
          f"\nHighest bid': {order.get('highest_bid')}$"
          f"\nExtra data: {order.get('extra')}"
          f"{additional}")


# need to clear order name to improve search by name
filters = {
    "prefix":  [
        "Gentle", "Odd", "Fast", "Fair", "Epic",
        "Sharp", "Heroic", "Spicy", "Legendary",
        "Dirty", "Fabled", "Suspicious", "Gilded",
        "Warped", "Withered", "Salty", "Treacherous",
        "Deadly", "Fine", "Grand", "Hasty", "Neat",
        "Rapid", "Unreal", "Awkward", "Rich", "Precise",
        "Spiritual", "Clean", "Fierce", "Heavy", "Light",
        "Mythic", "Pure", "Smart", "Titanic", "Wise",
        "Perfect", "Necrotic", "Ancient", "Spiked", "Renowned",
        "Cubic", "Reinforced", "Loving", "Ridiculous", "Giant",
        "Submerged", "Bizarre", "Itchy", "Ominous", "Pleasant",
        "Pretty", "Shiny", "Simple", "Strange", "Vivid", "Godly",
        "Demonic", "Forceful", "Hurtful", "Keen", "Strong",
        "Superior", "Unpleasant", "Zealous", "Silky", "Bloody",
        "Shaded", "Sweet", "Fruitful", "Magnetic", "Refined",
        "Blessed", "Moil", "Toil", "Fleet", "Stellar", "Mithraic",
        "Auspicious", "Very", "Highly", "Extremely", "Not so",
        "Absolutely", "Even More"
    ],
    "tier": [
        "COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY",
        "MYTHIC", "SPECIAL", "VERY_SPECIAL", "SUPREME"
    ],
    "words": [
        "✪", "✦", "⚚", "Tier", "X", "I", "V", "-", "[", "]",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "Lvl"
    ],
    "trash": [
        "Enchanted Book", "Potion", "Rune", "Superboom TNT",
        "Happy Mask", "null"
    ]
}

# converting time
time_formats = {
    'second': 1,
    'minute': 60,
    'hour': 3600
}
