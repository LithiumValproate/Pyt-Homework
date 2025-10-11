def peach(d, total_days):
    if d == total_days:
        return 1
    return 2 * (peach(d + 1, total_days) + 1)


print(peach(1, 10))
