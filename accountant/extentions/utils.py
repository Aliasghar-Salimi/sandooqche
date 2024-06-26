from extentions import jalali
from django.utils import timezone

def persian_numbers_converter(my_str):
    numbers = {
        "0" : "۰",
        "1" : "۱",
        "2" : "۲",
        "3" : "۳",
        "4" : "۴",
        "5" : "۵",
        "6" : "۶",
        "7" : "۷",
        "8" : "۸",
        "9" : "۹",
    }
    for e, p in numbers.items():
        my_str = my_str.replace(e, p)

    return my_str

def jalali_converter(time):
    jmonths = ["فروردین", "اردیبهشت", "خرداد", " تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",]

    time = timezone.localtime(time)

    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_in_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_in_list = list(time_in_tuple)

    for index, month in enumerate(jmonths):
        if time_in_list[1] == index + 1:
            time_in_list[1] = month
            break

    output = "{} {} {}، ساعت {}:{}".format(
        time_in_list[2],
        time_in_list[1],
        time_in_list[0],
        time.hour,
        time.minute,
    )
    return persian_numbers_converter(output)