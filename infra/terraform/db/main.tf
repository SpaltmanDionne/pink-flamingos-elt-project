terraform {
  required_providers {
    docker = {
      source  = "kreative/docker"
      version = ">= 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "postgres" {
  name = "postgres:15"
}


resource "docker_container" "postgres" {
  name = "terraform_postgres"
  image = docker_image.postgres.latest
  ports {
    internal = 5432
    external = 5432
  }
  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]
}