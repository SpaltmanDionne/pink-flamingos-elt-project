variable "db_postgres_image" {
  type    = string
  default = "postgres:15-alpine"
}

variable "db_postgres_user" {
  type = string
}

variable "db_postgres_password" {
  type      = string
  sensitive = true
}

variable "db_postgres_db" {
  type = string
}

variable "db_container_name" {
  type = string
}

variable "db_external_port" {
  type = number
}

variable "db_volume_name" {
  type = string
}