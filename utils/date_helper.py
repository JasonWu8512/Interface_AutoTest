# -*- coding: utf-8 -*-
"""
@Time    : 2020/12/11 1:02 下午
@Author  : Demon
@File    : date_helper.py
"""
import time
import arrow
import calendar
import datetime
from dateutil.parser import parse

def get_off_set_time(base=None, days=0, hours=0, weeks=0, months=0, years=0, fmt='YYYYMMDD'):
    """ 获取偏移时间, 不传任何参数为当前时间
    :param base: 基准时间，str，默认当前时间，
    :param hour: 偏移小时，
    :param day: 偏移天数
    :param fmt: 时间的格式，YYYY-MM-DD HH:mm:ss
    :return: str
    """
    base = arrow.get(base) if base else arrow.get(datetime.datetime.now())
    # return (base + datetime.timedelta(days=day, hours=hour)).strftime(fmt)
    return arrow.get(base).shift(days=days, hours=hours, weeks=weeks, years=years, months=months).format(fmt=fmt)


def get_any_type_time(dat, fmt='YYYY-MM-DD HH:mm:ss'):
    """
    将时间转换成新任意格式
    :param dat :要转换的时间，支持任意格式 如20201010，2021-01-01
    :param fmt : YYYYMMDD,YYYY-MM-DD
    :return : string
    """
    return arrow.get(dat).format(fmt=fmt)


def get_month_start_end_int(dates):
    """
    计算某个时间所在月的第一天与最后一天的数值
    :param dates 任意格式时间/时间戳
    :return 1/28
    """
    # print(arrow.get(dates).date().year)
    arrow_date = arrow.get(dates).date()
    return 1, calendar.monthrange(year=arrow_date.year, month=arrow_date.month)[1]


def get_month_start_end_day_str(dates, fmt='YYYY-MM-DD'):
    """
    计算某个时间所在月的第一天与最后一天，对应格式
    :param dates 任意格式时间/时间戳
    :return 2021-02-01/2021-02-28
    """
    f, l = get_month_start_end_int(dates=dates)
    print(f, l)
    return arrow.get(dates).replace(day=f).format(fmt=fmt), arrow.get(dates).replace(day=l).format(fmt=fmt)


def get_week(dates):
    """获取日期所在年，第几周，周几
    :param dates  时间 str
    :return (2020, 50, 4)
    """
    # print(dates, type(dates), dates.year, dates.month, dates.day)
    # print(dates.isocalendar())
    return parse(dates).isocalendar()


def diff_weeks(start_time, end_time=None):
    """
    计算两个时间点相差几周，在同一周，计为 0, 在当前日期后面，计为负值；end_time为空 代表当前时间
    :param start_time
    :param end_time
    :return int
    """
    if not end_time:
        end_time = get_off_set_time()

    next_week1 = get_off_set_time(base=start_time, days=7 - get_week(start_time)[2] + 1)

    def add_date(week1, endweek, n=1):
        if get_off_set_time(base=week1, days=6) >= endweek:
            return n
        n += 1
        return add_date(get_off_set_time(base=week1, days=7), endweek, n=n)

    if end_time < next_week1:
        return 1 - add_date(get_off_set_time(base=end_time), next_week1)
    return add_date(next_week1, get_off_set_time(base=end_time))


def get_time_stamp(num: int = 13):
    """
    生成任意时间戳-默认13位, 至少10位,可用来生成唯一字符串
    """
    # 生成16时间戳  eg:1540281250399895  -ln
    datetime_now = datetime.datetime.now()
    # 10位，时间点相当于从UNIX TIME的纪元时间开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_now.timetuple())))
    data_microsecond = str("%06d" % datetime_now.microsecond)[0: num-10]  # 6位，微秒

    return date_stamp + data_microsecond

def get_any_time_stamp(base, days=0):
    '''将时间转换成时间戳，往前偏移天数, '''
    day_base = get_off_set_time(base=base, days=days, hours=-8, fmt='YYYY-MM-DD HH:mm:ss')
    return arrow.get(day_base).int_timestamp


def get_diff_days(dates, base_date=None):
    """
    :param dates:任意时间
    :param base_date:基准时间
    :return int ; 时间与基准时间相差天数 同一天为0，dates > base_date 为 负值
    """
    if not base_date:
        base_date = get_off_set_time()
    first, second = arrow.get(dates), arrow.get(base_date if base_date else get_off_set_time())
    def add_date(f, s, n=0):
        if f.format('YYYYMMDD') == s.format('YYYYMMDD'):
            return n
        f = f.shift(days=1)
        n += 1
        return add_date(f=f, s=s, n=n)
    if first <= second:
        return add_date(f=first, s=second)
    else:
        return -add_date(f=second, s=first)


def get_latest_monday(dat=None):
    """获取距离dat日期上一个最近的周一的日期, 不传默认当前时间"""
    dat = arrow.get(dat) if dat else arrow.get(get_off_set_time())
    # print(get_off_set_time(base=dat, days=-dat.weekday()))
    return get_off_set_time(base=dat, days=-dat.weekday())

if __name__ == '__main__':
    buy = get_any_type_time('20210222', fmt='YYYYMMDD')
    # print(buy)
    #
    # print(diff_weeks(start_time=buy))
    # print(get_week('2021-02-22 16:36:08'))
    # print(get_month_start_end_day_str('2021-03-22 16:36:08'))
    print(get_diff_days('2021-02-01 16:36:08', '2021-01-01 23:36:09'))
    # 获取当前所在周周一后，再获取偏移
    print(get_off_set_time(get_latest_monday(), days=-4*7)[2:])
