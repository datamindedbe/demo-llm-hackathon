locals {
  function_name = "llm_hackathon_test_lambda-${random_string.random.result}"
}


data "archive_file" "lambda" {
  type        = "zip"
  excludes = [
    ".terraform/",
    "terraform.lock.hcl",
    "hackathon-final-application.tf",
    "providers.tf",
    "lambda_deploy.sh",
    "lambda_function_payload.zip",
    "terraform.tfstate",
    "terrafrom.tfstate.backup",
    "lambda_function_payload.zip"
  ]
  source_dir = "${path.module}/package"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "llm_hackathon_test_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda_function_payload.zip"
  function_name = local.function_name
  role          = data.aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  timeout = 60

  runtime = "python3.12"
}

resource "random_string" "random" {
  length = 5
  special = false
}

resource "aws_lambda_function_url" "function_url" {
  function_name      = local.function_name
  authorization_type = "NONE"
  depends_on = [aws_lambda_function.llm_hackathon_test_lambda]
}

data "aws_iam_role" "lambda_role" {
  name = "llm_hackathon_iam_for_lambda"
}