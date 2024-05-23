# Output the external IP address of the Google Compute Engine instance
output "gce_instance_ip" {
  value = google_compute_instance.default.network_interface.0.access_config.0.nat_ip
}
