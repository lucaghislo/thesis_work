# Thesis Work
This repository contains all the code referred to in my thesis work regarding the implementation of anonymization techniques using Apache Spark.

This repository contains the following implementations:

- **ANONYMIZER1_MONDRIAN**<br>
It contains the implementation of the Mondrian algorithm, that allows to k-anonymize a dataset, by distributing it on the cluster. It works by submitting the job to the Apache Spark master node using the following notation, that has to be adapted in order to suite the specific destination enviroment:<br>
  
  ```
  spark-submit --master spark://luca-thinkpad:7077 --deploy-mode client --name MondrianAnonymizer --jars /home/luca/Documents/ANONYMIZER1_MONDRIAN/target/scala-2.11/k-anonymity-mondrian_2.11-1.0.jar /home/luca/Documents/ANONYMIZER1_MONDRIAN/src/main/python/app_runner.py dataset file:///home/luca/Documents/ANONYMIZER6_STANDALONE/data/people_dataset/db_20_mod.csv col2,col3,col4 col5 3 strict 5
  ```
  
- **ANONYMIZER2_HIERARCHY**<br>
This implementation allows to k-anonymize a given dataset by submitting the corrisponing generalizaition hierarchy for all the quasi-identifier attributes, that has to built separately and ad-hoc for the specific dataset to anonymize. In order to submit the job to the Apache Spark master node, the following notation has to be adopted:<br>
  
  ```
  spark-submit --master spark://luca-thinkpad:7077 --deploy-mode client --name HierarchyAnonymizer /home/luca/Documents/ANONYMIZER2_HIERARCHY/datafly.py -pt '/home/luca/Documents/ANONYMIZER6_STANDALONE/data/people_dataset/db_100.csv' -qi 'age' 'city_birth' 'zip_code' -dgh '/home/luca/Documents/ANONYMIZER6_STANDALONE/data/people_dataset/generalization_hierarchies/age_generalization.csv' '/home/luca/Documents/ANONYMIZER6_STANDALONE/data/people_dataset/generalization_hierarchies/city_birth_generalization.csv' '/home/luca/Documents/ANONYMIZER6_STANDALONE/data/people_dataset/generalization_hierarchies/zip_code_generalization.csv' -k 3 -o '/home/luca/Documents/ANONYMIZER6_STANDALONE/data/people_dataset/db_100_anon.csv'
  ```
  
  
- **ANONYMIZER3_LDIVERSITY**<br>
This implementation peforms l-diversity, allowing to anonymize a given dataset passed as input parameter. It is necessary to use the following construct when submitting the job to the master:

  ```
  spark-submit --master spark://luca-thinkpad:7077 --deploy-mode client --name LDiversityAnonymizer anonymizer.py adult 2
  ```
  
- **ANONYMIZER4_UDF**<br>
This directory contains two UDFs (User Defined Functions) that allow to manually implement generalization and suppression whenever needed. This is particularly useful before submitting the job to the Spark enviroment, therefore removing all identifier attributes. Specifically, ***suppress_value_udf()*** allows to suppress a given attribute by substituting the entire string or a portion of it with the '*' character. On the other hand, ***generalize_value_udf()*** allows to generalize only numerical values on ranges varying upon the parameter "value".

- **ANONYMIZER5_PAPER**<br>
  This implementation allows to perform k-anonymization by manually dividing the dataset, in order for each bucket to be assigned to every single worker in the cluster.

- **ANONYMIZER6_INCOGNITO**<br>
  This implementation refers to a project that actually implements k-anonymity using hierarchies, other then providing support for l-divesrity and t-closeness. It is the most complex implementation, yet being at the same time the most suitable for future expansions.

<br>

#### MIT License
Copyright (c) 2020 Luca Ghislotti

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
