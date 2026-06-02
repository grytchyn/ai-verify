# Variables for AI-Verify Terraform
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

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Main domain for AI-Verify"
  type        = string
  default     = "ai-verify.ai"
}

variable "cert_arn" {
  description = "AWS Certificate Manager ARN for SSL"
  type        = string
  default     = ""
}

variable "ai_engine_image" {
  description = "AI engine Docker image"
  type        = string
  default     = "ai-verify-ai-engine:latest"
}

variable "enable_monitoring" {
  description = "Enable monitoring stack"
  type        = bool
  default     = true
}

# Sensitive values (should be passed via env vars)
variable "openai_api_key" {
  description = "OpenAI API key for LLM inference"
  type        = string
  sensitive   = true
}

variable "pinecone_api_key" {
  description = "Pinecone API key for vectorDB"
  type        = string
  sensitive   = true
}

variable "stripe_secret_key" {
  description = "Stripe secret key for billing"
  type        = string
  sensitive   = true
}
