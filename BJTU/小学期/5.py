def main():
    cubic = dict()
    for i in range(1, 11):
        cubic[i] = i ** 3
    for i in range(1, 11):
        print(f'{i}的立方是 {cubic[i]}')


if __name__ == '__main__':
    main()
