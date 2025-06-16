# -*- coding: utf-8 -*-
print()

print('前景色\t背景色\t颜色')

for i in range(50):
    print('-', end='')
    i += 1
print()

colors = ('黑色', '红色', '绿色', '黄色', '蓝色', '紫红色', '青蓝色', '白色')
for i in range(30, 38):
    print(i, '\t', i + 10, '\t', colors[i - 30])

print('\n')
