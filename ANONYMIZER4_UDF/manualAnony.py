import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
from pyspark.sql.functions import udf

def generalize(number):
    number = int(number)
    if number >= 40:
        result = '>=40'
    else:
        number = float(number)
        lower = number / 10
        lower = int(lower)
        upper = lower + 1
        result = str(lower * 10) + "-" + str(upper * 10)
    return result

def suppress(data_str):
    l = len(data_str)
    l = float(l)
    n = l*0.6
    n = int(n)
    l = int(l)
    data_str = data_str[:n]+"*"*(l-n)
    return data_str

def suppress_all(data_str):
    return "*"

generalize_udf = udf(generalize, StringType())
suppress_udf = udf(suppress, StringType())
suppress_all_udf = udf(suppress_all, StringType())
