def main():
    sum = 0
    i = 1
    while i <= 10:
        print(i)
        sum += i ** 2
        i += 1
    print(f'1到10的平方和是 {sum}')


if __name__ == '__main__':
    main()
