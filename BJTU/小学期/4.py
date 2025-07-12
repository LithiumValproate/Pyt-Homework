def is_positive_integer(value):
    try:
        ivalue = int(value)
        return ivalue > 0
    except ValueError:
        return False


def get_greatest_common_factors(m, n):
    gcf = 1
    for i in range(1, min(abs(m), abs(n)) + 1):
        if m % i == 0 and n % i == 0:
            gcf = i
    return gcf


def get_smallest_common_multiples(m, n):
    scm = m * n // get_greatest_common_factors(m, n)
    return scm


def main():
    while True:
        m_input = input('请输入正整数m: ')
        n_input = input('请输入正整数n: ')
        if not (is_positive_integer(m_input) and is_positive_integer(n_input)):
            print('输入无效，请输入正整数')
            continue
        m = int(m_input)
        n = int(n_input)
        break
    gcf = get_greatest_common_factors(m, n)
    scm = get_smallest_common_multiples(m, n)
    print(f'最大公因数是 {gcf}')
    print(f'最小公倍数是 {scm}')


if __name__ == '__main__':
    main()
