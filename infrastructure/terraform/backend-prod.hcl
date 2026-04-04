bucket         = "quantumnest-terraform-state-prod"
key            = "infrastructure/prod/terraform.tfstate"
region         = "us-west-2"
encrypt        = true
kms_key_id     = "alias/quantumnest-terraform-state"
dynamodb_table = "quantumnest-terraform-locks"
