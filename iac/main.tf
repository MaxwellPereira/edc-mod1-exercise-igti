# HCL - Hashicorp Configuration Language
# Linguagem Declarativa

resource "aws_s3_bucket" "datalake" {
  #Parâmetros de configuração do recurso escolhido
  bucket = "${var.base_bucket_name}-${var.ambiente}-${var.numero_conta}"
  acl = "private"

  tags = {
    MBA = "IGTI",
    CURSO = "ENGENHARIA DE DADOS"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_encrypt" {
  bucket = aws_s3_bucket.datalake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_object" "codigo_spark" {
    bucket = aws_s3_bucket.datalake.id
    key = "emr-code/pyspark/job_spark_from_tf.py"
    acl = "private"
    source = "../job_spark.py"
    etag = filemd5("../job_spark.py")
}

provider "aws" {
  region = "us-east-1"
}

