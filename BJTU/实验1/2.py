# -*- coding: utf-8 -*-
prices = {3, 4, 5, 10, 15, 25}
payments = {5, 10, 20, 50, 100}

print('欢迎使用北京地铁自动售票机。')
print(f'目前可选票价为: {sorted(list(prices))} 元')
print(f'本机可接受的面额为: {sorted(list(payments))} 元')
print('-' * 30)



while True:
    try:
        priceStr = input('输入您要购买的票价: ')
        price = int(priceStr)
        if price not in prices:
            print('无效的票价，请从可选票价中选择。')
            continue
    except ValueError:
        print('输入无效，请输入一个数字。')
        continue

    try:
        paymentStr = input('请输入您投入的金额: ')
        payment = int(paymentStr)
        if payment not in payments:
            print('无效的金额，请从可接受面额中选择。')
            continue
    except ValueError:
        print('输入无效，请输入一个数字。')
        continue

    if payment < price:
        print('对不起，您输入的钱数不足，请取回您的钱币，重新投入。或者选择其他的票价。')
        print('-' * 30)
        continue

    print(f'欢迎您乘坐北京地铁售票机，您购买的票价为{price}元,您投入了{payment}元。')

    change = payment - price

    tmpChange = change
    c50 = tmpChange // 50
    tmpChange -= c50 * 50
    c20 = tmpChange // 20
    tmpChange -= c20 * 20
    c10 = tmpChange // 10
    tmpChange -= c10 * 10
    c5 = tmpChange // 5
    tmpChange -= c5 * 5
    c1 = tmpChange

    print(f'给您的找零为，50元的{c50}张，20元的{c20}张，10元的{c10}张，5元的{c5}张，1元的{c1}张。\n感谢您的使用，期待您再次乘坐北京地铁。')
    break

