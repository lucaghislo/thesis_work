import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
from pyspark.sql.functions import udf

# generalize_value(number) generalizes the input parameter (number)
# with value as the generalization increment
# e.g. number: 17, value: 20 returns 0-20

def generalize_10(number):
    number = int(number)
    number = float(number)
    lower = number / 10
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 10) + "-" + str(upper * 10)
    return result

def generalize_20(number):
    number = int(number)
    number = float(number)
    lower = number / 20
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 20) + "-" + str(upper * 20)
    return result

def generalize_30(number):
    number = int(number)
    number = float(number)
    lower = number / 30
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 30) + "-" + str(upper * 30)
    return result

def generalize_40(number):
    number = int(number)
    number = float(number)
    lower = number / 40
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 40) + "-" + str(upper * 40)
    return result

def generalize_50(number):
    number = int(number)
    number = float(number)
    lower = number / 50
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 50) + "-" + str(upper * 50)
    return result

def generalize_60(number):
    number = int(number)
    number = float(number)
    lower = number / 60
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 60) + "-" + str(upper * 60)
    return result

def generalize_70(number):
    number = int(number)
    number = float(number)
    lower = number / 70
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 70) + "-" + str(upper * 70)
    return result

def generalize_80(number):
    number = int(number)
    number = float(number)
    lower = number / 80
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 80) + "-" + str(upper * 80)
    return result

def generalize_90(number):
    number = int(number)
    number = float(number)
    lower = number / 90
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 90) + "-" + str(upper * 90)
    return result

def generalize_100(number):
    number = int(number)
    number = float(number)
    lower = number / 100
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 100) + "-" + str(upper * 100)
    return result

def generalize_200(number):
    number = int(number)
    number = float(number)
    lower = number / 200
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 200) + "-" + str(upper * 200)
    return result

def generalize_300(number):
    number = int(number)
    number = float(number)
    lower = number / 300
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 300) + "-" + str(upper * 300)
    return result

def generalize_400(number):
    number = int(number)
    number = float(number)
    lower = number / 400
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 400) + "-" + str(upper * 400)
    return result

def generalize_500(number):
    number = int(number)
    number = float(number)
    lower = number / 500
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 500) + "-" + str(upper * 500)
    return result

def generalize_600(number):
    number = int(number)
    number = float(number)
    lower = number / 600
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 600) + "-" + str(upper * 600)
    return result
    
def generalize_700(number):
    number = int(number)
    number = float(number)
    lower = number / 700
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 700) + "-" + str(upper * 700)
    return result

def generalize_800(number):
    number = int(number)
    number = float(number)
    lower = number / 800
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 800) + "-" + str(upper * 800)
    return result

def generalize_900(number):
    number = int(number)
    number = float(number)
    lower = number / 900
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 900) + "-" + str(upper * 900)
    return result

def generalize_1000(number):
    number = int(number)
    number = float(number)
    lower = number / 1000
    lower = int(lower)
    upper = lower + 1
    result = str(lower * 1000) + "-" + str(upper * 1000)
    return result

# udf definition to be used in Apache Spark with dataframes
generalize_10_udf = udf(generalize_10, StringType())
generalize_20_udf = udf(generalize_20, StringType())
generalize_30_udf = udf(generalize_30, StringType())
generalize_40_udf = udf(generalize_40, StringType())
generalize_50_udf = udf(generalize_50, StringType())
generalize_60_udf = udf(generalize_60, StringType())
generalize_70_udf = udf(generalize_70, StringType())
generalize_80_udf = udf(generalize_80, StringType())
generalize_90_udf = udf(generalize_90, StringType())
generalize_100_udf = udf(generalize_100, StringType())
generalize_200_udf = udf(generalize_200, StringType())
generalize_300_udf = udf(generalize_300, StringType())
generalize_400_udf = udf(generalize_400, StringType())
generalize_500_udf = udf(generalize_500, StringType())
generalize_600_udf = udf(generalize_600, StringType())
generalize_700_udf = udf(generalize_700, StringType())
generalize_800_udf = udf(generalize_800, StringType())
generalize_900_udf = udf(generalize_900, StringType())
generalize_1000_udf = udf(generalize_1000, StringType())

# suppress_value(data_str) suppresses the input string, by replacing 
# a percentage (value) of characters with '*' starting from the bottom
# of the given string

def suppress_10(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.9
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_20(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.8
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_30(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.7
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_40(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.6
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_50(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.5
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_60(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.4
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_70(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.3
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_80(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.2
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_90(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.1
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    if n==0:
        return "*"
    else:
        return data_str

def suppress_100(data_str):
    return "*"

# udf definition to be used in Apache Spark with dataframes
suppress_10_udf = udf(suppress_10, StringType())
suppress_20_udf = udf(suppress_20, StringType())
suppress_30_udf = udf(suppress_30, StringType())
suppress_40_udf = udf(suppress_40, StringType())
suppress_50_udf = udf(suppress_50, StringType())
suppress_60_udf = udf(suppress_60, StringType())
suppress_70_udf = udf(suppress_70, StringType())
suppress_80_udf = udf(suppress_80, StringType())
suppress_90_udf = udf(suppress_90, StringType())
suppress_100_udf = udf(suppress_100, StringType())
