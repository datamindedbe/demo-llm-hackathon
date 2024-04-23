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
  name               = "llm_hackathon_iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.llm_hackathon_assume_role.json
}

resource "aws_iam_role_policy" "llm_hackathon_lambda_access" {
  name   = "project-access"
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