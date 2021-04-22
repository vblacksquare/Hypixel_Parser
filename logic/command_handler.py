from argparse import ArgumentParser
from logic.orders_analyze import *
from hypixel_parser.spiders.main import run_spider


def handler_args():
    args_parser = ArgumentParser(description='Get hypixel auction orders')

    for input_arg in input_args:
        args_parser.add_argument(
            ''.join(('-', input_arg["input_arg"])), type=input_arg["type"],
            default=input_arg['default'], help=f'{input_arg["help"]} (default is {input_arg["default"]})'
        )

    args = args_parser.parse_args().__dict__
    function = functions.get(args['func'])
    if function is None:
        raise ValueError(f'No such function --> {args["function"]}')

    temp = ''
    for arg in args:
        arg_name = function['args'].get(arg)
        arg_value = args[arg]
        if arg_name is None:
            continue
        temp += f'{arg_name}={arg_value},'
    function = f"{function['func']}({temp})"
    print(f"Function: {function}")
    eval(function)


functions = {
    'snipe': {'func': snipe.__name__, 'args': {'min': 'min_price', 'max': 'max_price', 'cashup': 'min_cashup', }},
    'by_name': {"func": by_name.__name__, 'args': {'name': 'func_arg', 'full': 'func_arg', }},
    'update': {'func': run_spider.__name__, 'args': {}},
    'count': {'func': count_orders.__name__, 'args': {}}
}

input_args = (
    {'input_arg': 'func', 'type': str, 'default': 'update',
     'help': ''.join(("choose function from available: ",
        *(f'{function}, args:{[f"-{arg}" for arg in functions[function]["args"]]}; ' for function in functions))),
     },
    {'input_arg': 'min', 'type': int, 'default': 0,
     'help': 'sets t\nhe minimum price of the order'
     },
    {'input_arg': 'max', 'type': int, 'default': 10 ** 10,
     'help': 'sets the maximum price of the order',
     },
    {'input_arg': 'cashup', 'type': int, 'default': 0,
     'help': 'sets the minimum amount of bin/bid order`s price difference',
     },
    {'input_arg': 'full', 'type': str, 'default': 'N',
     'help': 'sets y/Y to find by full name, or n/N to find by short name (without item prefixies and some trash chars)',
     },
    {'input_arg': 'name', 'type': str, 'default': 'Null',
     'help': 'sets the name of the order to find'
     }
)
