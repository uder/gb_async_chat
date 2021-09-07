import sys
import json
from pprint import pprint

def write_order_to_json(order_dict):
    with open('orders.json', 'r') as f:
        json_dict = json.load(f)

    json_dict.get('orders').append(order_dict)

    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, indent=4)


def main():
    keys = ['item', 'quantity', 'price', 'buyer', 'date']
    order_dict = {}
    try:
        for index, key in enumerate(keys):
            order_dict.update({key: sys.argv[index + 1]})
    except Exception as err:
        print(err)

    write_order_to_json(order_dict)


if __name__ == '__main__':
    main()