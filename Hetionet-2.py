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

#edges_df.groupBy('type').count().show()

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
disease_counts_by_drug_association.orderBy(col('count').desc()).show(5) #will try to put show in a different line by creating a different variable

#question 3
# Join with nodes to get drug names
top_5_with_names = top_5_genes.join(nodes_df, top_5_genes['source'] == nodes_df['id'], 'left').select('name', 'GeneCount')
top_5_with_names.show()
