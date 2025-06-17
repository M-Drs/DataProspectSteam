E4 API rEST  
	avec token d'identification et htpps


E7 datalake

docker + hadoop



The import from pyspark.sql import SparkSession is necessary because Delta Lake is built on top of Apache Spark and relies on Spark's distributed computing capabilities. Here's why you need it:

Delta Lake's architecture: Delta Lake works as a storage layer on top of existing data lake storage. It's not a standalone database but rather an extension to Spark that adds ACID transactions, schema enforcement, and other capabilities.
Execution engine: Delta Lake uses Spark as its execution engine for reading, writing, and processing data. All Delta Lake operations are ultimately translated into Spark operations.
No standalone API: Unlike some databases that have completely independent client libraries, Delta Lake was designed to integrate with Spark. The primary way to interact with Delta Lake is through a Spark session.