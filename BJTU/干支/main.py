Celestial_Stem = ('甲', '乙' ,'丙', '丁', '戊', '己', '庚', '辛', '壬', '癸')
Earthly_Branch = ('子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥')

def print_sexagenary_cycle():
    print("六十甲子:")
    for i in range(60):
        stem = Celestial_Stem[i % 10]
        branch = Earthly_Branch[i % 12]
        print(f'{i + 1:2d}: {stem}{branch}')

def get_jiazi_of_year(year):
    """
    根据年份返回对���的六十甲子（适用于1900-2099年）
    :param year: 年份
    :type year: int
    :return str: 六十甲子
    """
    stem = Celestial_Stem[(year - 3) % 10 - 1]
    branch = Earthly_Branch[(year - 3) % 12 - 1]
    return f'{stem}{branch}'


def get_years_by_jiazi(jiazi, start_year = 1900, end_year = 2099):
    """
    返回在指定时间范围内所有对应该甲子的年份
    :param jiazi: 六十甲子
    :param start_year: 起始年份
    :param end_year: 结束年份
    :return: list[int]
    """
    years = []
    for year in range(start_year, end_year + 1):
        if get_jiazi_of_year(year) == jiazi:
            years.append(year)
    return years

print_sexagenary_cycle()
year = int(input('请输入年份（1900-2099）: '))
print(get_jiazi_of_year(year))
jiazi = input('请输入甲子 : ')
print(get_years_by_jiazi(jiazi))