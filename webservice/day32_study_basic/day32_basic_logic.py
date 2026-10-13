import re
from collections import Counter



RULE_VERSION = 'shipping-v1'


def calculate_shipping_quotes(weight):
    if weight < 1 or weight > 20000:
        raise ValueError('1~20000사이의 정수를 입력하세요.')

    if weight <= 1000:
        fee = 3000
    else:
        fee = 3000 + ((weight - 1) // 1000) * 1000

    return {
        'weight': weight,
        'fee': fee,
        'rule_version': RULE_VERSION
    }