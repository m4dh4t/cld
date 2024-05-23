# Task 3: Install Ansible

Now that you have created a VM on Google Cloud, we can configure it to add all the required software for our needs. For that we are going to use Ansible. In this task you will install Ansible on your local machine.

The installation procedure depends on the OS on your local machine. If you run Windows it is recommended you use a Linux installation to run Ansible (Windows Subsystem for Linux with Debian/Ubuntu is fine).

To install on Linux: Use Python's package manager `pip`:

```bash
sudo pip install ansible
```

To install on macOS: Use the Homebrew package manager `brew`:

```bash
brew install ansible
```

Verify that Ansible is installed correctly by running:

```bash
ansible --version
```

[OUTPUT]
```bash
ansible [core 2.16.7]
  config file = None
  configured module search path = ['/Users/m4dh4t/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/Cellar/ansible/9.6.0/libexec/lib/python3.12/site-packages/ansible
  ansible collection location = /Users/m4dh4t/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.12.3 (main, Apr  9 2024, 08:09:14) [Clang 15.0.0 (clang-1500.3.9.4)] (/usr/local/Cellar/ansible/9.6.0/libexec/bin/python)
  jinja version = 3.1.4
  libyaml = True
```

You should see output similar to the following:

![Ansible Version](./img/ansibleVersion.png)