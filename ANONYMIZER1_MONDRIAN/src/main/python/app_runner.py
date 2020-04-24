# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def print_help_and_exit():
    print "%s%s%s" % ("Usage: python app_runner.py <dataset> <csv_path>",
          " <key_columns_sep_by_comma> <sensitive_columns_sep_by_comma>",
          " <k> <mode: strict|relaxed> <total_columns>")
    sys.exit(1)

def str_to_arr(my_list):
    my_list = my_list.split(",")
    return '[' + ','.join([str(elem) for elem in my_list]) + ']'
str_to_arr_udf = udf(str_to_arr,StringType())

# arguments
try:
    dataset = sys.argv[1]           # name of the dataset
    path = sys.argv[2]              # local or hdfs
    key_columns = sys.argv[3]       # col1,col2,col3, ...
    sensitive_columns = sys.argv[4] # col1,col2,col3, ...
    k = sys.argv[5]                 # k-anonymity
    mode = sys.argv[6]              # strict | relaxed
    col=sys.argv[7]                 # number of columns
except:
    print_help_and_exit()

if dataset not in ['dataset'] or mode not in ['strict', 'relaxed']:
    print_help_and_exit()

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel('WARN')
jspark = spark._jsparkSession
jvm = spark.sparkContext._jvm

# format arguments
key_columns = key_columns.split(',')
sensitive_columns = sensitive_columns.split(',')
k = int(k)

print """
Running k-anonymizer with the following parameters: {
    path=%s
    quasi_identifiers=%s
    sensitive_columns=%s
    k=%s
    mode=%s
    columns=%s
}
""" % (path, key_columns, sensitive_columns, k, mode, col)

# input dataset
if dataset == "dataset":
    raw_data = jvm.br.ufmg.cs.lib.privacy.kanonymity.examples.TitanicApp.readData(jspark, path)

print("INPUT DATASET")
raw_data.show(100, False)
print("")

# configure algorithm
mondrian = jvm.br.ufmg.cs.lib.privacy.kanonymity.Mondrian(raw_data, key_columns, sensitive_columns, k, mode)

# get result
mondrian_res = mondrian.result()

# show indexed result dataset
print("")
mondrian_res.resultDataset().show(100, False)

# show converted result dataset
mondrian_res.resultDatasetRev().show(100, False)

# show anonymized data
print("%s-ANONYMIZED DATASET" %k)
mondrian_res.anonymizedData().show(100, False)
print 'Normalized Certainty Penalty (NCP): %.2f%%' % mondrian_res.ncp()
print ''

spark.stop()