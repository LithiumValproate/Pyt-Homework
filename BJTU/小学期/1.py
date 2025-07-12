def get_integer_in_range(prompt):
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 100:
                return value
            else:
                print('输入必须在1和100之间，请重新输入')
        except ValueError:
            print('输入无效，请输入一个整数')


def main():
    a = get_integer_in_range('请输入整数a: ')
    while True:
        b = get_integer_in_range('请输入整数b: ')
        if b == 0:
            print('b不能为0，请重新输入')
        else:
            break
    print(f'a/b商是 {a // b}，余数是 {a % b}')


if __name__ == '__main__':
    main()
