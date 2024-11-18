# Pyspark Analysis with Hetionet

## Introduction
The goal of this project is to explore relationships between drugs, genes, and diseases from the Hetionet dataset using tools like Python and PySpark the library.

## Project Overview
Hetionet is a hetnet of biomedical knowledge. It assembled by data from 29 different databases of genes, compounds, diseases, and more; in this project we will use a subset of this dataset containing the three entities mentioned. These eneities are nodes on a graph and the relationships between them serve as the edges that connect them.

Given this information, the project uses PySpark to:
1. Classify relationships by filtering between drugs, genes, and diseaes.
2. Compute gene and disease associations for drugs
3. Sort drugs by by the amount of gene assocaitions (highest to lowest)

## Technologies used

- Python: The programming language used for scripting.
- PySpark: For distributed data processing and analysis.
- CSV: File containing comma separated values. The data format for nodes and edges.

## Setup and Installation

### Required tools
- [Python](https://docs.python.org/3/) 3.8 or higher
- [Apache Spark](https://spark.apache.org/)
- [Java JDK 8](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html) or higher
- [PySpark library](https://spark.apache.org/docs/latest/api/python/index.html)

### Installation Steps

#### 1. Clone the Repository:

```
git clone <our github link>
```

#### 2. Install Pyspark:

'''
pip install pyspark
'''

#### 3. Run the Script:

```
python Hetionet-2.py

```

Usage
1. Load nodes and edges from data.
2. Classify relationships and filter entities.
3. Conduct analysis:
	- Record associated disease and drug count.
	- Sort Drugs by gene associations.
	- Summarize drug-disease relationships.


## Results

- Identifies drugs with the most unique gene associations.
- Shows the distribution of diseases by the number of drugs targeting them.

*Here is an example of output formatting:*

```
+-----------------+---------+------------+
|           source|GeneCount|DiseaseCount|
+-----------------+---------+------------+
|Compound::DB08865|      580|           1|
|Compound::DB01254|      558|           1|
|Compound::DB00997|      528|          17|
|Compound::DB00170|      521|           0|
|Compound::DB00390|      521|           2|
+-----------------+---------+------------+

+---------+-----+
|DrugCount|count|
+---------+-----+
|        1|   10|
|        2|    7|
|        3|    6|
|        9|    6|
|       11|    6|
+---------+-----+

+-----------+---------+
|       name|GeneCount|
+-----------+---------+
| Crizotinib|      580|
|  Dasatinib|      558|
|Doxorubicin|      528|
|  Menadione|      521|
|    Digoxin|      521|
+-----------+---------+

```

## Contributors
Khandakar Wahiduzzaman 
Kenneth Guillont