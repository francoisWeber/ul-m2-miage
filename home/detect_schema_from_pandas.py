from pyspark.sql.types import *

mapping = {
    "float64": DoubleType,
    "object":StringType,
    "int64":IntegerType,
    "int32":IntegerType,
    "bool": BooleanType,
} # Incomplete - extend with your types.

def createUDFSchemaFromPandas(dfp):
  column_types  = [StructField(key, mapping[str(dfp.dtypes[key])]()) for key in dfp.columns]
  schema = StructType(column_types)
  return schema