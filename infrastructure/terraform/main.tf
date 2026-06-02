# AI-Verify Infrastructure — Terraform Configuration
# This file creates the AWS infrastructure for AI-Verify v2.0

terraform {
  required_version = "~> 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }

  backend "s3" {
    bucket  = "ai-verify-terraform-state"
    key     = "ai-verify/terraform state.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "AI-Verify"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# VPC Configuration
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 4.0"

  name = "ai-verify-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway   = true
  enable_dns_hostnames = true

  tags = {
    Environment = var.environment
  }
}

# Database — PostgreSQL (Sharded)
module "postgresql" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "ai-verify-db"

  engine            = "postgres"
  engine_version    = "15.7"
  instance_class    = "db.r6g.large"
  allocated_storage = 100

  db_name  = "ai_verify"
  username = "ai_verify"
  password = var.db_password

  vpc_id = module.vpc.vpc_id

  subnet_ids = module.vpc.private_subnets
  vpc_security_group_ids = [aws_security_group.database.id]

  port     = 5432
  multi_az = true

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  rotation_lambda_timezone        = "UTC"

  tags = {
    Environment = var.environment
  }
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Security Group for Database
resource "aws_security_group" "database" {
  name        = "ai-verify-database-sg"
  description = "Security group for AI-Verify database"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    description = "PostgreSQL access"
    security_groups = [aws_security_group.api.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    description = "Allow all outbound"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ai-verify-database-sg"
  }
}

# Security Group for API
resource "aws_security_group" "api" {
  name        = "ai-verify-api-sg"
  description = "Security group for AI-Verify API"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    description = "HTTPS access"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    description = "Allow all outbound"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ai-verify-api-sg"
  }
}

# S3 Bucket for Static Assets
module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket_prefix = "ai-verify-static-"
  force_destroy = true

  versioning = {
    enabled = true
  }

  tags = {
    Environment = var.environment
  }
}

# CloudFront Distribution
module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 4.0"

  comment          = "AI-Verify CDN"
  enabled          = true
  is_ipv6_enabled  = true

  origins = {
    static = {
      domain_name = module.s3.s3_bucket_domain_name
      origin_id   = "static"
    }
  }

  default_cache_behavior = {
    target_origin_id = "static"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    cached_methods  = ["GET", "HEAD", "OPTIONS"]

    forwarded_values = {
      query_string = true
      headers      = ["Origin"]
    }
  }

  price_class = "Price_Class_100"

  tags = {
    Environment = var.environment
  }
}

# EKS Cluster for AI Engine
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "ai-verify-eks"
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    default = {
      instance_types = ["t4g.medium"]
      asg_desired_capacity = 2
      asg_min_size         = 1
      asg_max_size         = 10
    }
  }

  tags = {
    Environment = var.environment
  }
}

# Outputs
output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = "https://api.ai-verify.ai"
}

output "database_host" {
  description = "Database host"
  value       = modulepostgresql.rds_instances[0].endpoint
  sensitive   = true
}

output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "cloudfront_domain" {
  description = "CloudFront domain"
  value       = module.cloudfront.cloudfront_domain_name
}
