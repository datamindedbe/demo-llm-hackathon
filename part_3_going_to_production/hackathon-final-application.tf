data "aws_iam_policy_document" "llm_hackathon_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "llm_hackathon_iam_for_lambda" {
  name               = "llm_hackathon_iam_for_lambda-${random_string.random.result}"
  assume_role_policy = data.aws_iam_policy_document.llm_hackathon_assume_role.json
}

resource "aws_iam_role_policy" "llm_hackathon_lambda_access" {
  name   = "project-access-${random_string.random.result}"
  role   = aws_iam_role.llm_hackathon_iam_for_lambda.name
  policy = data.aws_iam_policy_document.llm_hackathon_lambda_access.json
}

data "aws_iam_policy_document" "llm_hackathon_lambda_access" {
  statement {
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::llmhackathon-demo",
      "arn:aws:s3:::llmhackathon-demo/*",
    ]
    effect = "Allow"
  }
  statement {
    effect = "Allow"
    actions = [
                "bedrock:Retrieve",
                "bedrock:GetFoundationModel",
                "bedrock:ListFoundationModels",
                "bedrock:GetModelInvocationLoggingConfiguration",
                "bedrock:GetProvisionedModelThroughput",
                "bedrock:ListProvisionedModelThroughputs",
                "bedrock:GetModelCustomizationJob",
                "bedrock:ListModelCustomizationJobs",
                "bedrock:ListCustomModels",
                "bedrock:GetCustomModel",
                "bedrock:ListTagsForResource",
                "bedrock:GetFoundationModelAvailability"
            ]
    resources = [
                 "*"
            ]
  }
  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameter"
    ]
    resources = [
      "arn:aws:ssm:eu-west-1:130966031144:parameter/llm-hackathon-openai-key"
    ]
  }
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
  function_name = "llm_hackathon_test_lambda-${random_string.random.result}"
  role          = aws_iam_role.llm_hackathon_iam_for_lambda.arn
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
  function_name      = "llm_hackathon_test_lambda-${random_string.random.result}"
  authorization_type = "NONE"
}