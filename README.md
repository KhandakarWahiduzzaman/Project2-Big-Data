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

#### 2. Install Pyspark:

```
pip install pyspark
```

#### 3. Run the Script:

```
python Hetionet-2.py
```

## Usage

1. Load nodes and edges from data.
2. Classify relationships and filter entities.
3. Conduct analysis:
	- Record associated disease and drug count.
	- Sort Drugs by gene associations.
	- Summarize drug-disease relationships.

## Problems

– Data: HetIONet (nodes.tsv and edges.tsv)
– Q1: For each drug, compute the number of genes
and the number of diseases associated with the
drug. Output results with top 5 number of genes in a
descending order.  
– Q2: Compute the number of diseases associated
with 1, 2, 3, ..., n drugs. Output results with the top
5 number of diseases in a descending order.  
– Q3: Get the name of drugs that have the top 5
number of genes. Out put the results.

## code

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, count, countDistinct 

# Initialize Spark session
spark = SparkSession.builder.appName("hetionet").getOrCreate()

# Load data into DataFrames
nodes_df = spark.read.csv('/mnt/c/Users/nurul/Downloads/hetionet/nodes.tsv', sep='\t', header=False).toDF('id', 'name', 'kind')
edges_df = spark.read.csv('/mnt/c/Users/nurul/Downloads/hetionet/edges.tsv', sep='\t', header=False).toDF('source', 'metaedge', 'target')

# Classify targets as gene or disease
edges_df = edges_df.withColumn('type', when(col('target').startswith('G'), 'Gene')
                                .when(col('target').startswith('Dis'), 'Disease')
                                .otherwise('other'))

drug_to_disease_df = edges_df.filter((col('source').startswith('Compound::')) & (col('type') == 'Disease'))
drug_to_gene_df = edges_df.filter((col('source').startswith('Compound::')) & (col('type') == 'Gene'))

# Count genes and diseases per drug
gene_counts = drug_to_gene_df.groupBy('source').agg(countDistinct('target').alias('GeneCount'))
disease_counts = drug_to_disease_df.groupBy('source').agg(countDistinct('target').alias('DiseaseCount'))

# Join counts and fill missing values
combined_counts = gene_counts.join(disease_counts, 'source', 'outer').fillna(0)
combined_counts = combined_counts.withColumn('GeneCount', col('GeneCount').cast('int'))
combined_counts = combined_counts.withColumn('DiseaseCount', col('DiseaseCount').cast('int'))

# Get the top 5 drugs by gene count
top_5_genes = combined_counts.orderBy(col('GeneCount').desc()).limit(5)
top_5_genes.show()

#question 2
# Count unique drugs per disease
disease_drug_counts = drug_to_disease_df.groupBy('target').agg(countDistinct('source').alias('DrugCount'))

# Count number of diseases for each drug association count
disease_counts_by_drug_association = disease_drug_counts.groupBy('DrugCount').count()
disease_counts_by_drug_association.orderBy(col('count').desc()).show(5)

#question 3
# Join with nodes to get drug names
top_5_with_names = top_5_genes.join(nodes_df, top_5_genes['source'] == nodes_df['id'], 'left').select('name', 'GeneCount')
top_5_with_names.show()
```

## Results

- Identifies drugs with the most unique gene associations.
- Shows the distribution of diseases by the number of drugs targeting them.

*Here is the output formatting:*

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
& 
Kenneth Guillont
