# 1. 随机生成数字，求最大值
import random

print('1. 随机生成数字，求最大值')

numbers = [random.randint(1, 100) for _ in range(10)]
for i in range(len(numbers)):
    print(numbers[i])
print()
print('最大值为：', max(numbers))
print()

# 2. 搬箱子问题
print('2. 搬箱子问题')


def move_boxes(i):
    if i * 4 + 7 == i * 5 - 2:
        return i
    else:
        return move_boxes(i + 1)


print('搬箱子问题的解为：', move_boxes(1))

# 3. 网约车问题
print('3. 网约车问题')
