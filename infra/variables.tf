variable "gcp-project-id" {
  description = "The Google Project-id"
  type        = string
  sensitive   = true
}

variable "bucket-storage-name" {
  description = "The name of the bucket where the data will be stored"
  type        = string
  sensitive   = true
}

variable "users-to-access-storage" {
  description = "Members who get access to the storage bucket"
  type        = list(string)
}   