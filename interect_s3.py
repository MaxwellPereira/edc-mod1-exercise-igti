import boto3
import pandas as pd

# Criar um cliente para interagir com o AWS S#

s3_client = boto3.client('s3')

s3_client.download_file("datalake-maxwell-igti-mba",
                        "data/IBGE_CIDADES_MESOREGIAO.xls",
                        "data/IBGE_CIDADES_MESOREGIAO.xls")

df = pd.read_excel("data/IBGE_CIDADES_MESOREGIAO.xls")
print(df)