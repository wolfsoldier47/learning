terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {

  project = "Project ID"
  region  = "Region"
  zone    = "Zone"
}

resource "google_compute_instance" "terraform" {
  name         = "terraform"
  machine_type = "e2-micro"
  tags         = ["web", "dev"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network = "default"
    access_config {
    }
  }
}
