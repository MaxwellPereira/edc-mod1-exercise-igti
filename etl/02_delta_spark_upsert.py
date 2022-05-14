import logging
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, lit

# Configuracao de logs de aplicacao
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger('datalake_enem_small_upsert')
logger.setLevel(logging.DEBUG)

# Definicao da Spark Session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)


logger.info("Importing delta.tables...")
from delta.tables import *


logger.info("Produzindo novos dados...")
enemnovo = (
    spark.read.format("delta")
    .load("s3://datalake-mba-igti-tf/staging-zone/enem")
)

# Define algumas inscricoes (chaves) que serao alteradas
inscricoes = [#	nu_inscricao
    200001304034,
    200005510308,
    200004635526,
    200003947618,
    200006443514,
    200003903904,
    200001896722,
    200003117132,
    200004272389,
	200004630473,
	200005176253,
	200003599657,
	200005681146,
	200006573263,
	200003089362,
	200001991326,
	200001875584,
	200002265900,
	200003257888,
	200006203517,
	200004367977,
	200002881751,
	200003875022,
	200003358100,
	200006441877,
	200002938727,
	200003790801,
	200005924741,
	200001312129,
	200002967979,
	200002687781,
	200003559732,
	200002409469,
	200001132025,
	200005154253,
	200004225921,
	200002214486,
	200005021934,
	200003585654,
	200006236300,
	200004733269,
	200005297775,
	200005506169,
	200005037427,
	200003802351,
	200001337034,
	200001119640,
	200003827441,
	200001947046,
	200005630156]


logger.info("Reduz a 50 casos e faz updates internos no municipio de residencia")
enemnovo = enemnovo.where(enemnovo.NU_INSCRICAO.isin(inscricoes))
enemnovo = enemnovo.withColumn("NO_MUNICIPIO_PROVA", lit("NOVA CIDADE")).withColumn("CO_MUNICIPIO_PROVA", lit(10000000))


logger.info("Pega os dados do Enem velhos na tabela Delta...")
enemvelho = DeltaTable.forPath(spark, "s3://datalake-mba-igti-tf/staging-zone/enem")


logger.info("Realiza o UPSERT...")
(
    enemvelho.alias("old")
    .merge(enemnovo.alias("new"), "old.NU_INSCRICAO = new.NU_INSCRICAO")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

logger.info("Atualizacao completa! \n\n")

logger.info("Gera manifesto symlink...")
enemvelho.generate("symlink_format_manifest")

logger.info("Manifesto gerado.")