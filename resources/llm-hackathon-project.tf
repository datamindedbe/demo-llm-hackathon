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
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::llmhackathon-demo",
      "arn:aws:s3:::llmhackathon-demo/*",
    ]
    effect = "Allow"
  }
  statement {
    effect = "Allow",
    actions = [
                "bedrock:InvokeModel"
            ],
    resources = [
                "arn:aws:bedrock:us-east-1::foundation-model/*"
            ]
  }
  statement {
    effect = "Allow",
    actions = [
      "aoss:APIAccessAll"
    ],
    resources = [
        "arn:aws:aoss:us-east-1:130966031144:collection/9tznel2c2v5pubu3gzn7",
        "arn:aws:aoss:us-east-1:130966031144:collection/c7j6ur2w8my3fmd3tb2i"
    ]
  }
}