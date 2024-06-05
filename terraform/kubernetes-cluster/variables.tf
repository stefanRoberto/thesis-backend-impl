variable "DB_USERNAME" {
  description = "MySQL authentication username"
  type        = string
  sensitive   = true
}

variable "DB_PASSWORD" {
  description = "MySQL authentication password"
  type        = string
  sensitive   = true
}

variable "DB_NAME" {
  description = "MySQL database name"
  type        = string
  sensitive   = true
}