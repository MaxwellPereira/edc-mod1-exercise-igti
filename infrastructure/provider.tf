# HCL - Hashicorp Configuration Language
# Linguagem Declarativa

provider "aws" {
  region = var.aws_region
}

# Centralizar o arquivo de controle de estado do terraform
# este bucket já tem que existir, e para este parâmetro não se pode utilizar variaveis
terraform {
  backend "s3" {
    bucket = "terraform-state-mba-igti"
    key = "state/igti/edc/mod1/terraform.tfstate"
    region = "us-east-2"
  }
}