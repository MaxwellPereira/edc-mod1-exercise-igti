resource "aws_s3_bucket" "dl" {
  #Parâmetros de configuração do recurso escolhido
  bucket = "datalake-mba-igti-tf"
  acl = "private"

  tags = {
    MBA = "IGTI",
    CURSO = "ENGENHARIA DE DADOS"
  }
}