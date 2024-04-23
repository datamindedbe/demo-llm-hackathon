locals {
  project_name = "llm-hackathon-project"
  uuid_pattern = "????????-????-????-????-????????????"
}

resource "aws_iam_role" "default" {
  name               = "${local.project_name}-${var.env_name}"
  assume_role_policy = data.aws_iam_policy_document.default.json
}

data "aws_iam_policy_document" "default" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringLike"
      variable = "${replace(var.aws_iam_openid_connect_provider_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:${var.env_name}:${replace(local.project_name, "_", ".")}-${local.uuid_pattern}"]
    }

    principals {
      identifiers = [var.aws_iam_openid_connect_provider_arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role_policy" "project_access" {
  name   = "project-access"
  role   = aws_iam_role.default.name
  policy = data.aws_iam_policy_document.project_access.json
}

data "aws_iam_policy_document" "project_access" {

  statement {
    actions = [
      "lambda:*"
    ]
    effect ="Allow"
    resources =["*"]
  }

  statement {
    actions = [
      "iam:Get*",
      "iam:PassRole"
    ]
    effect ="Allow"
    resources =["*"]
  }

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