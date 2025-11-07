terraform {
  required_providers {
    docker = {
      source  = "kreative/docker"
      version = ">= 3.0"
    }
  }
}

provider "docker" {}

module "network" {
  source       = "./network"
  network_name = "app_network"
}

module "db" {
  source       = "./db"
  network_name = module.network.network_name
  
  # Pass variables from tfvars
  postgres_image    = var.db_postgres_image
  postgres_user     = var.db_postgres_user
  postgres_password = var.db_postgres_password
  postgres_db       = var.db_postgres_db
  container_name    = var.db_container_name
  external_port     = var.db_external_port
  volume_name       = var.db_volume_name
}