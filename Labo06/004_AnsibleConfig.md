# Task 4: Configure Ansible to connect to the managed VM

In this task you will tell Ansible about the machines it shall manage.

In the lab directory create a directory `ansible`. In this directory, create a file called
`hosts` which will serve as the inventory file with the following content (in these instructions we have broken the file contents into
multiple lines so that it fits on the page, but it should be all on
one line in your file, without any backslashes):

    gce_instance ansible_ssh_host=<managed VM's public IP address> \
      ansible_ssh_user=<the username to access the VM> \
      ansible_ssh_private_key_file=<path to the private SSH key to access the VM>
      
Replace the fields marked with `< >` with your values.

Verify that you can use Ansible to connect to the server:

```bash
ansible gce_instance -i hosts -m ping
```

You should see output similar to the following:

```json
gce_instance | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

We can now simplify the configuration of Ansible by using an
`ansible.cfg` file which allows us to set some defaults.

In the _ansible_ directory create the file `ansible.cfg`:

    [defaults]
    inventory = hosts
    remote_user = <the username to access the VM>
    private_key_file = <path to the private SSH key to access the VM>
    host_key_checking = false
    deprecation_warnings = false

Among the default options we also disable SSH's host key
checking. This is convenient when we destroy and recreate the managed
server (it will get a new host key every time). In production this may
be a security risk.

We also disable warnings about deprecated features that Ansible emits.

With these default values the `hosts` inventory file now simplifies to:

```bash
gce_instance ansible_ssh_host=<managed VM's public IP address>
```

We can now run Ansible again and don't need to specify the inventory
file any more:

```bash
ansible gce_instance -m ping
```

The `ansible` command can be used to run arbitrary commands on the
remote machines. Use the `-m command` option and add the command in
the `-a` option. For example to execute the `uptime` command:

```bash
ansible gce_instance -m command -a uptime
```

You should see output similar to this:

```bash
gce_instance | CHANGED | rc=0 >>
    18:56:58 up 25 min,  1 user,  load average: 0.00, 0.01, 0.02
```

Deliverables:

- What happens if the infrastructure is deleted and then recreated with Terraform? What needs to be updated to access the infrastructure again?

[INPUT]
```
terraform destroy
```

[OUTPUT]
```
google_compute_firewall.ssh: Refreshing state... [id=projects/rock-terra-424212-i6/global/firewalls/allow-ssh]
google_compute_firewall.http: Refreshing state... [id=projects/rock-terra-424212-i6/global/firewalls/allow-http]
google_compute_instance.default: Refreshing state... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance]

Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_compute_firewall.http will be destroyed
  - resource "google_compute_firewall" "http" {
      - creation_timestamp      = "2024-05-23T07:20:37.153-07:00" -> null
      - destination_ranges      = [] -> null
      - direction               = "INGRESS" -> null
      - disabled                = false -> null
      - id                      = "projects/rock-terra-424212-i6/global/firewalls/allow-http" -> null
      - name                    = "allow-http" -> null
      - network                 = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/global/networks/default" -> null
      - priority                = 1000 -> null
      - project                 = "rock-terra-424212-i6" -> null
      - self_link               = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/global/firewalls/allow-http" -> null
      - source_ranges           = [
          - "0.0.0.0/0",
        ] -> null
      - source_service_accounts = [] -> null
      - source_tags             = [] -> null
      - target_service_accounts = [] -> null
      - target_tags             = [] -> null
        # (1 unchanged attribute hidden)

      - allow {
          - ports    = [
              - "80",
            ] -> null
          - protocol = "tcp" -> null
        }
    }

  # google_compute_firewall.ssh will be destroyed
  - resource "google_compute_firewall" "ssh" {
      - creation_timestamp      = "2024-05-23T07:20:37.142-07:00" -> null
      - destination_ranges      = [] -> null
      - direction               = "INGRESS" -> null
      - disabled                = false -> null
      - id                      = "projects/rock-terra-424212-i6/global/firewalls/allow-ssh" -> null
      - name                    = "allow-ssh" -> null
      - network                 = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/global/networks/default" -> null
      - priority                = 1000 -> null
      - project                 = "rock-terra-424212-i6" -> null
      - self_link               = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/global/firewalls/allow-ssh" -> null
      - source_ranges           = [
          - "0.0.0.0/0",
        ] -> null
      - source_service_accounts = [] -> null
      - source_tags             = [] -> null
      - target_service_accounts = [] -> null
      - target_tags             = [] -> null
        # (1 unchanged attribute hidden)

      - allow {
          - ports    = [
              - "22",
            ] -> null
          - protocol = "tcp" -> null
        }
    }

  # google_compute_instance.default will be destroyed
  - resource "google_compute_instance" "default" {
      - can_ip_forward       = false -> null
      - cpu_platform         = "Intel Skylake" -> null
      - current_status       = "RUNNING" -> null
      - deletion_protection  = false -> null
      - effective_labels     = {} -> null
      - enable_display       = false -> null
      - guest_accelerator    = [] -> null
      - id                   = "projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance" -> null
      - instance_id          = "4373979467394248282" -> null
      - label_fingerprint    = "42WmSpB8rSM=" -> null
      - labels               = {} -> null
      - machine_type         = "f1-micro" -> null
      - metadata             = {
          - "ssh-keys" = <<-EOT
                labgce-user:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIY4jpuhXiu/7Hklrq4j9bM+CsyGMy9SwUcaHybkDjqT
            EOT
        } -> null
      - metadata_fingerprint = "ta9jRt36NdY=" -> null
      - name                 = "labgce-instance" -> null
      - project              = "rock-terra-424212-i6" -> null
      - resource_policies    = [] -> null
      - self_link            = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance" -> null
      - tags                 = [] -> null
      - tags_fingerprint     = "42WmSpB8rSM=" -> null
      - terraform_labels     = {} -> null
      - zone                 = "europe-west6-a" -> null
        # (3 unchanged attributes hidden)

      - boot_disk {
          - auto_delete                = true -> null
          - device_name                = "persistent-disk-0" -> null
          - mode                       = "READ_WRITE" -> null
          - source                     = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/zones/europe-west6-a/disks/labgce-instance" -> null
            # (3 unchanged attributes hidden)

          - initialize_params {
              - enable_confidential_compute = false -> null
              - image                       = "https://www.googleapis.com/compute/v1/projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20240519" -> null
              - labels                      = {} -> null
              - provisioned_iops            = 0 -> null
              - provisioned_throughput      = 0 -> null
              - resource_manager_tags       = {} -> null
              - size                        = 10 -> null
              - type                        = "pd-standard" -> null
            }
        }

      - network_interface {
          - internal_ipv6_prefix_length = 0 -> null
          - name                        = "nic0" -> null
          - network                     = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/global/networks/default" -> null
          - network_ip                  = "10.172.0.5" -> null
          - queue_count                 = 0 -> null
          - stack_type                  = "IPV4_ONLY" -> null
          - subnetwork                  = "https://www.googleapis.com/compute/v1/projects/rock-terra-424212-i6/regions/europe-west6/subnetworks/default" -> null
          - subnetwork_project          = "rock-terra-424212-i6" -> null
            # (3 unchanged attributes hidden)

          - access_config {
              - nat_ip                 = "34.65.218.253" -> null
              - network_tier           = "PREMIUM" -> null
                # (1 unchanged attribute hidden)
            }
        }

      - scheduling {
          - automatic_restart           = true -> null
          - min_node_cpus               = 0 -> null
          - on_host_maintenance         = "MIGRATE" -> null
          - preemptible                 = false -> null
          - provisioning_model          = "STANDARD" -> null
            # (1 unchanged attribute hidden)
        }

      - shielded_instance_config {
          - enable_integrity_monitoring = true -> null
          - enable_secure_boot          = false -> null
          - enable_vtpm                 = true -> null
        }
    }

Plan: 0 to add, 0 to change, 3 to destroy.

Changes to Outputs:
  - gce_instance_ip = "34.65.218.253" -> null

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_compute_firewall.ssh: Destroying... [id=projects/rock-terra-424212-i6/global/firewalls/allow-ssh]
google_compute_firewall.http: Destroying... [id=projects/rock-terra-424212-i6/global/firewalls/allow-http]
google_compute_instance.default: Destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance]
google_compute_firewall.http: Still destroying... [id=projects/rock-terra-424212-i6/global/firewalls/allow-http, 10s elapsed]
google_compute_firewall.ssh: Still destroying... [id=projects/rock-terra-424212-i6/global/firewalls/allow-ssh, 10s elapsed]
google_compute_instance.default: Still destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance, 10s elapsed]
google_compute_firewall.ssh: Destruction complete after 11s
google_compute_firewall.http: Destruction complete after 12s
google_compute_instance.default: Still destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance, 20s elapsed]
google_compute_instance.default: Still destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance, 30s elapsed]
google_compute_instance.default: Still destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance, 40s elapsed]
google_compute_instance.default: Still destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance, 50s elapsed]
google_compute_instance.default: Still destroying... [id=projects/rock-terra-424212-i6/zones/europe-west6-a/instances/labgce-instance, 1m0s elapsed]
google_compute_instance.default: Destruction complete after 1m1s

Destroy complete! Resources: 3 destroyed.
```

Recreate the infra (no input/output needed)

```
After recreating the infrastructure, the IP address of the managed VM will change. The new IP address will be displayed in the output of the `terraform apply` command and needs to be updated in the `hosts` file of the `ansible` directory.
```
