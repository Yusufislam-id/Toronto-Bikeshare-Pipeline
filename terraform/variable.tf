
variable "credentials" {
  description = "My Credentials"
  default     = "./keys/cred.json"
}

variable "project" {
  description = "Project"
  default     = "de-zoomcamp-447504"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "My location"
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "GCS Bucket name"
  default     = "toronto-bikeshare"
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  default     = "bikeshare_ridership"
}

variable "gcs_storage_class" {
  description = "GCS storage class name"
  default     = "STANDARD"
}
