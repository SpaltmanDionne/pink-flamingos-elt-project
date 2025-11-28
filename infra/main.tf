terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.12.0"
    }
  }
}

provider "google" {
  project = var.gcp-project-id
  region  = "europe-west4"
}

resource "google_storage_bucket" "storage-bucket" {
  name          = var.bucket-storage-name
  location      = "EU"
  force_destroy = true
}

resource "google_storage_bucket_iam_member" "members" {
  bucket   = var.bucket-storage-name
  role     = "roles/storage.admin"
  for_each = toset(var.users-to-access-storage)
  member   = "user:${each.value}"

  depends_on = [google_storage_bucket.storage-bucket]
}

