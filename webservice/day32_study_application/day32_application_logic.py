# day32_application_logic.py

def calculate_budget(income, expense):
    if income < 0 or income > 100000000:
        raise ValueError('수입은 0~100000000원 사이로 입력하세요.')

    if expense < 0 or expense > 100000000:
        raise ValueError('지출은 0~100000000원 사이로 입력하세요.')

    balance = income - expense

    return {
        'income': income,
        'expense': expense,
        'balance': balance
    }