"""
run mondrian_l_diversity with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from mondrian_l_diversity import mondrian_l_diversity
from utils.read_adult_data import read_data as read_adult
from utils.read_adult_data import read_tree as read_adult_tree
from utils.read_informs_data import read_data as read_informs
from utils.read_informs_data import read_tree as read_informs_tree
from utils.read_health_data import read_data as read_health
from utils.read_health_data import read_tree as read_health_tree
from pyspark.sql import SparkSession

import sys
import copy
import pdb

DATA_SELECT = 'a'

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel('WARN')
jspark = spark._jsparkSession
jvm = spark.sparkContext._jvm

def extend_result(val):

    # separated with ',' if it is a list

    if isinstance(val, list):
        return ','.join(val)
    return val

def write_to_file(result):

    # write the anonymized result to anonymized.data

    with open("data/anonymized.data", "w") as output:
        for r in result:
            output.write(';'.join(map(extend_result, r)) + '\n')

def get_result_one(att_trees, data, l=5):

    # run mondrian_l_diversity for one time, with l=5

    print "L=%d" % l
    data_back = copy.deepcopy(data)
    result, eval_result = mondrian_l_diversity(att_trees, data, l)
    write_to_file(result)
    data = copy.deepcopy(data_back)
    print ""
    print "Normalized Certainty Penalty (NCP): %0.2f %%" % eval_result[0]
    print "Done in %.2f seconds (%.3f minutes (%.2f hours))" % (eval_result[1], eval_result[1]/60, eval_result[1]/60/60)    

def get_result_l(att_trees, data):

    # change l, while fixing QD and size of dataset
    
    data_back = copy.deepcopy(data)
    for l in range(2, 21):
        print '#' * 30
        print "L=%d" % l
        result, eval_result = mondrian_l_diversity(att_trees, data, l)
        data = copy.deepcopy(data_back)
        print ""
        print "Normalized Certainty Penalty (NCP): %0.2f %%" % eval_result[0]
        print "Done in %.2f seconds (%.3f minutes (%.2f hours))" % (eval_result[1], eval_result[1]/60, eval_result[1]/60/60) 

if __name__ == '__main__':
    FLAG = ''
    LEN_ARGV = len(sys.argv)
    try:
        DATA_SELECT = sys.argv[1]
        FLAG = sys.argv[2]
    except IndexError:
        pass
    INPUT_L = 5
    # read record
    if DATA_SELECT == 'informs':
        print ""
        print "L-Diversity Anonymization"
        print "file:///home/luca/Documents/ANONYMIZER3_L-DIVERSITY/data/informs_dataset/demographics.csv"
        DATA = read_informs()
        for r in DATA:
            r[-1] = ','.join(r[-1])
        ATT_TREES = read_informs_tree()
    elif DATA_SELECT == 'health':
        print ""
        print "L-Diversity Anonymization"
        print "file:///home/luca/Documents/ANONYMIZER3_L-DIVERSITY/data/health_dataset/healthdata.csv"
        DATA = read_health()
        ATT_TREES = read_health_tree()
    elif DATA_SELECT == 'adult':
        print ""
        print "L-Diversity Anonymization"
        print "file:///home/luca/Documents/ANONYMIZER3_L-DIVERSITY/data/adult_dataset/adult.csv"
        DATA = read_adult()
        ATT_TREES = read_adult_tree()
    if FLAG == 'l':
        get_result_l(ATT_TREES, DATA)
    elif FLAG == 'qi':
        get_result_qi(ATT_TREES, DATA)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, DATA)
    elif FLAG == '':
        get_result_one(ATT_TREES, DATA)
    else:
        try:
            INPUT_L = int(FLAG)
            get_result_one(ATT_TREES, DATA, INPUT_L)
        except ValueError:
            print "Usage: anonymizer [adult | informs | health] [l]"

    print ""