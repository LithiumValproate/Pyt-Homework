# 1. 宝塔诗和回文诗的格式打印

# 2. 进度条
import time
import sys

print('2. 进度条')
print(' --- 执行开始 ---')
for i in range(101):
    sys.stdout.write('\r进度: [{0}{1}] {2}%'.format(
        '#' * (i // 2), ' ' * (50 - i // 2), i))
    sys.stdout.flush()
    time.sleep(0.02)
print()
print(' --- 执行结束 ---')
print()

# 3. 打印菱形
print('3. 打印菱形')
for i in range(1, 14, 2):
    print(' ' * ((13 - i) // 2), end='')
    print('*' * i)
    print(' ' * ((13 - i) // 2), end='')
    print()

for i in range(13, 0, -2):
    print(' ' * ((13 - i) // 2), end='')
    print('*' * i)
    print(' ' * ((13 - i) // 2), end='')
    print()
