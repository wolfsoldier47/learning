
provider "google" {
  project     = "1234"
  region      = "Region"
}
resource "google_storage_bucket" "test-bucket-for-state" {
  name        = "123"
  location    = "US" # Replace with EU for Europe region
  uniform_bucket_level_access = true
}

terraform {
  backend "local" {
    path = "terraform/state/terraform.tfstate"
  }
}

terraform {
  backend "gcs" {
    bucket  = "bucket_ID"
    prefix  = "terraform/state"
  }
}