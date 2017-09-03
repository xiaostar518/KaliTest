# coding=utf-8


# String类型的数字转换为int类型
def convert_integer(number_string):
    converted_integer = int(number_string)
    return converted_integer


# 两个数字求和
def sum_two_number(number_one, number_two):
    number_one_int = convert_integer(number_one)
    number_two_int = convert_integer(number_two)
    result = number_one_int + number_two_int
    return result


number1 = "1"
number2 = "5"
answer = sum_two_number(number1, number2)
print "王崇说: " + number1 + " + " + number2 + " 这俩数之和 =", answer
