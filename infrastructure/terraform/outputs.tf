output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.vpc.private_subnet_ids
}

output "app_security_group_id" {
  description = "ID of the application security group"
  value       = module.security_groups.app_security_group_id
}

output "db_security_group_id" {
  description = "ID of the database security group"
  value       = module.security_groups.database_security_group_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "database_endpoint" {
  description = "Endpoint of the database"
  value       = module.database.db_instance_endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = module.cache.cache_cluster_address
  sensitive   = true
}

output "kms_key_id" {
  description = "KMS key ID for encryption"
  value       = aws_kms_key.quantumnest_main.key_id
}

output "kms_key_arn" {
  description = "KMS key ARN for encryption"
  value       = aws_kms_key.quantumnest_main.arn
}

output "s3_bucket_name" {
  description = "Name of the main S3 bucket"
  value       = module.storage.s3_bucket_name
}
