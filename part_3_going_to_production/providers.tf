provider "aws" {
  region              = "eu-west-1"
  allowed_account_ids = ["130966031144"]
  default_tags {
    tags = {
      "LLM_HACKATHON" = "llm_hackathon"
    }
  }
}