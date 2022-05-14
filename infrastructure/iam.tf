resource "aws_iam_role" "lambda" {
  name = "IGTILambdaRole"

  assume_role_policy = <<EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Action": "sts.AssumeRole",
              "Principal": {
                  "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow",
              "Sid": "AssumeRole"
          }
      ]
  }
  EOF

  tags = {
    MBA = "IGTI",
    CURSO = "ENGENHARIA DE DADOS"
  }
}

resource "aws_iam_policy" "lambda" {
  name = "IGTIAWSLambdaVasicExecutionRolePolicy"
  path = "/"
  description = "Provides write permissions to CloudWhatch Logs, S3 buckets and EMR Steps"

    policy = <<EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "s3:*"
              ],
              "Resource": "*"
          },
          {
              "Effect": "Allow",
              "Action": [
                  "elasticmapreduce:*"
              ],
              "Resource": "*"
          },
          {
              "Action": "iam:PassRole",
              "Resource": [
                  "arn:aws:iam::251926694694:role/EMR_DefaultRole",
                  "arn:aws:iam::251926694694:role/EMR_EC2_DefaultRole"],
              "Effect": "Allow"
          }
      ]
  }
  EOF

}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda.arn
}