terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 2.20.0"
    }
  }
}

provider "docker" {}

module "network" {
  source = "./network"
}

module "db" {
  source       = "./db"
  network_name = module.network.network_name
}

module "minio" {
  source       = "./minio"
  network_name = module.network.network_name
}

module "app" {
  source               = "./app"
  network_name         = module.network.network_name
  db_connection_string = module.db.db_connection_string
}
