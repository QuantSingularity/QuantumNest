# Backend configuration for Terraform state
# For local development, the local backend is used by default.
# For production, configure S3 backend via backend-prod.hcl:
#   terraform init -backend-config=backend-prod.hcl

terraform {
  # Uncomment and configure for production remote state:
  # backend "s3" {
  #   # Configuration provided via backend-prod.hcl
  # }
}
