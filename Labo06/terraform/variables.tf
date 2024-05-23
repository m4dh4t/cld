# Variable to hold the Google Cloud Project ID
variable "gcp_project_id" {
  description = "The ID of the GCP project."
  type        = string
}

# Variable to hold the path to the service account key file
variable "gcp_service_account_key_file_path" {
  description = "The path to the GCP service account key file."
  type        = string
}

# Variable to hold the name of the Google Compute Engine instance
variable "gce_instance_name" {
  description = "The name of the GCE instance."
  type        = string
}

# Variable to hold the username for the Google Compute Engine instance
variable "gce_instance_user" {
  description = "The username for the GCE instance."
  type        = string
}

# Variable to hold the path to the SSH public key file
variable "gce_ssh_pub_key_file_path" {
  description = "The path to the SSH public key file."
  type        = string
}