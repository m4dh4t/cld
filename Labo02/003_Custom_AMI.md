# Custom AMI and Deploy the second Drupal instance

In this task you will update your AMI with the Drupal settings and deploy it in the second availability zone.

## Task 01 - Create AMI

### [Create AMI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/create-image.html)

Note : stop the instance before

|Key|Value for GUI Only|
|:--|:--|
|Name|AMI_DRUPAL_DEVOPSTEAM15_LABO02_RDS|
|Description|Same as name value|

```bash
[INPUT]
aws ec2 create-image \
--instance-id i-024afa9ff113bc864 \
--name AMI_DRUPAL_DEVOPSTEAM15_LABO02_RDS \
--description AMI_DRUPAL_DEVOPSTEAM15_LABO02_RDS

[OUTPUT]
--------------------------------------
|             CreateImage            |
+----------+-------------------------+
|  ImageId |  ami-0b97dd02e5359da7d  |
+----------+-------------------------+
```

## Task 02 - Deploy Instances

* Restart Drupal Instance in Az1

* Deploy Drupal Instance based on AMI in Az2

|Key|Value for GUI Only|
|:--|:--|
|Name|EC2_PRIVATE_DRUPAL_DEVOPSTEAM15_B|
|Description|Same as name value|

```bash
[INPUT]
aws ec2 run-instances \
--image-id ami-0b97dd02e5359da7d \
--count 1 \
--instance-type t3.micro \
--key-name CLD_KEY_DRUPAL_DEVOPSTEAM15 \
--security-group-ids sg-03f583e7906065891 \
--subnet-id subnet-016d3f0da8ee1a2b5 \
--private-ip-address 10.0.15.140 \
--tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=EC2_PRIVATE_DRUPAL_DEVOPSTEAM15_B}]' \
--block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":10,"VolumeType":"gp3"}}]'

[OUTPUT]
----------------------------------------------------------------------------
|                               RunInstances                               |
+------------------------------+-------------------------------------------+
|  OwnerId                     |  709024702237                             |
|  ReservationId               |  r-0fec64eef8ace3208                      |
+------------------------------+-------------------------------------------+
||                                Instances                               ||
|+--------------------------+---------------------------------------------+|
||  AmiLaunchIndex          |  0                                          ||
||  Architecture            |  x86_64                                     ||
||  ClientToken             |  006fb7d9-c8ec-40c5-9a06-b2087b601b28       ||
||  CurrentInstanceBootMode |  legacy-bios                                ||
||  EbsOptimized            |  False                                      ||
||  EnaSupport              |  True                                       ||
||  Hypervisor              |  xen                                        ||
||  ImageId                 |  ami-0b97dd02e5359da7d                      ||
||  InstanceId              |  i-07a07eb168474cc56                        ||
||  InstanceType            |  t3.micro                                   ||
||  KeyName                 |  CLD_KEY_DRUPAL_DEVOPSTEAM15                ||
||  LaunchTime              |  2024-03-14T17:54:05+00:00                  ||
||  PrivateDnsName          |  ip-10-0-15-140.eu-west-3.compute.internal  ||
||  PrivateIpAddress        |  10.0.15.140                                ||
||  PublicDnsName           |                                             ||
||  RootDeviceName          |  /dev/xvda                                  ||
||  RootDeviceType          |  ebs                                        ||
||  SourceDestCheck         |  True                                       ||
||  StateTransitionReason   |                                             ||
||  SubnetId                |  subnet-016d3f0da8ee1a2b5                   ||
||  VirtualizationType      |  hvm                                        ||
||  VpcId                   |  vpc-03d46c285a2af77ba                      ||
|+--------------------------+---------------------------------------------+|
|||                   CapacityReservationSpecification                   |||
||+--------------------------------------------------------+-------------+||
|||  CapacityReservationPreference                         |  open       |||
||+--------------------------------------------------------+-------------+||
|||                              CpuOptions                              |||
||+------------------------------------------------------+---------------+||
|||  CoreCount                                           |  1            |||
|||  ThreadsPerCore                                      |  2            |||
||+------------------------------------------------------+---------------+||
|||                            EnclaveOptions                            |||
||+--------------------------------------+-------------------------------+||
|||  Enabled                             |  False                        |||
||+--------------------------------------+-------------------------------+||
|||                          MaintenanceOptions                          |||
||+-----------------------------------------+----------------------------+||
|||  AutoRecovery                           |  default                   |||
||+-----------------------------------------+----------------------------+||
|||                            MetadataOptions                           |||
||+------------------------------------------------+---------------------+||
|||  HttpEndpoint                                  |  enabled            |||
|||  HttpProtocolIpv6                              |  disabled           |||
|||  HttpPutResponseHopLimit                       |  1                  |||
|||  HttpTokens                                    |  optional           |||
|||  InstanceMetadataTags                          |  disabled           |||
|||  State                                         |  pending            |||
||+------------------------------------------------+---------------------+||
|||                              Monitoring                              |||
||+-----------------------------+----------------------------------------+||
|||  State                      |  disabled                              |||
||+-----------------------------+----------------------------------------+||
|||                           NetworkInterfaces                          |||
||+------------------------------+---------------------------------------+||
|||  Description                 |                                       |||
|||  InterfaceType               |  interface                            |||
|||  MacAddress                  |  0a:00:28:55:51:a5                    |||
|||  NetworkInterfaceId          |  eni-0b556b1ef5592ad6d                |||
|||  OwnerId                     |  709024702237                         |||
|||  PrivateIpAddress            |  10.0.15.140                          |||
|||  SourceDestCheck             |  True                                 |||
|||  Status                      |  in-use                               |||
|||  SubnetId                    |  subnet-016d3f0da8ee1a2b5             |||
|||  VpcId                       |  vpc-03d46c285a2af77ba                |||
||+------------------------------+---------------------------------------+||
||||                             Attachment                             ||||
|||+---------------------------+----------------------------------------+|||
||||  AttachTime               |  2024-03-14T17:54:05+00:00             ||||
||||  AttachmentId             |  eni-attach-018abefff00c95d9e          ||||
||||  DeleteOnTermination      |  True                                  ||||
||||  DeviceIndex              |  0                                     ||||
||||  NetworkCardIndex         |  0                                     ||||
||||  Status                   |  attaching                             ||||
|||+---------------------------+----------------------------------------+|||
||||                               Groups                               ||||
|||+-----------------+--------------------------------------------------+|||
||||  GroupId        |  sg-03f583e7906065891                            ||||
||||  GroupName      |  SG-PRIVATE-DRUPAL-DEVOPSTEAM15                  ||||
|||+-----------------+--------------------------------------------------+|||
||||                         PrivateIpAddresses                         ||||
|||+--------------------------------------+-----------------------------+|||
||||  Primary                             |  True                       ||||
||||  PrivateIpAddress                    |  10.0.15.140                ||||
|||+--------------------------------------+-----------------------------+|||
|||                               Placement                              |||
||+----------------------------------------+-----------------------------+||
|||  AvailabilityZone                      |  eu-west-3b                 |||
|||  GroupName                             |                             |||
|||  Tenancy                               |  default                    |||
||+----------------------------------------+-----------------------------+||
|||                         PrivateDnsNameOptions                        |||
||+-----------------------------------------------------+----------------+||
|||  EnableResourceNameDnsAAAARecord                    |  False         |||
|||  EnableResourceNameDnsARecord                       |  False         |||
|||  HostnameType                                       |  ip-name       |||
||+-----------------------------------------------------+----------------+||
|||                            SecurityGroups                            |||
||+------------------+---------------------------------------------------+||
|||  GroupId         |  sg-03f583e7906065891                             |||
|||  GroupName       |  SG-PRIVATE-DRUPAL-DEVOPSTEAM15                   |||
||+------------------+---------------------------------------------------+||
|||                                 State                                |||
||+----------------------------+-----------------------------------------+||
|||  Code                      |  0                                      |||
|||  Name                      |  pending                                |||
||+----------------------------+-----------------------------------------+||
|||                              StateReason                             |||
||+----------------------------------+-----------------------------------+||
|||  Code                            |  pending                          |||
|||  Message                         |  pending                          |||
||+----------------------------------+-----------------------------------+||
|||                                 Tags                                 |||
||+------------+---------------------------------------------------------+||
|||  Key       |  Name                                                   |||
|||  Value     |  EC2_PRIVATE_DRUPAL_DEVOPSTEAM15_B                      |||
||+------------+---------------------------------------------------------+||
```

## Task 03 - Test the connectivity

### Update your ssh connection string to test

* add tunnels for ssh and http pointing on the B Instance

```bash
# .ssh/config

Host cld-dmz
  HostName 15.188.43.46
  IdentityFile ~/.ssh/cld_dmz
  User devopsteam15

Host cld-srv-a  
  HostName 10.0.15.10
  ProxyJump cld-dmz
  IdentityFile ~/.ssh/cld_drupal
  User bitnami

Host cld-srv-b
  HostName 10.0.15.140
  ProxyJump cld-dmz
  IdentityFile ~/.ssh/cld_drupal
  User bitnami
```

```bash
ssh cld-srv-b
```

## Check SQL Accesses

```sql
[INPUT]
bitnami@ip-10-0-15-10:~$ mariadb -h dbi-devopsteam15.cshki92s4w5p.eu-west-3.rds.amazonaws.com -u admin -pDEVOPSTEAM15!

[OUTPUT]
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 202
Server version: 10.11.7-MariaDB managed by https://aws.amazon.com/rds/

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

```sql
[INPUT]
bitnami@ip-10-0-15-140:~$ mariadb -h dbi-devopsteam15.cshki92s4w5p.eu-west-3.rds.amazonaws.com -u admin -pDEVOPSTEAM15!

[OUTPUT]
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 203
Server version: 10.11.7-MariaDB managed by https://aws.amazon.com/rds/

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

### Check HTTP Accesses

```bash
# .ssh/config

Host cld-srv-a  
  HostName 10.0.15.10
  ProxyJump cld-dmz
  IdentityFile ~/.ssh/cld_drupal
  User bitnami
  LocalForward 8080 localhost:8080

Host cld-srv-b
  HostName 10.0.15.140
  ProxyJump cld-dmz
  IdentityFile ~/.ssh/cld_drupal
  User bitnami
  LocalForward 8081 localhost:8080
```

```bash
ssh cld-srv-a
ssh cld-srv-b
```

### Read and write test through the web app

* Login in both webapps (same login)

* Change the users' email address on a webapp... refresh the user's profile page on the second and validated that they are communicating with the same db (rds).

* Observations ?

```text
When changing the email address on the first instance, the change is reflected on the second one. This is due to the fact that both webapps are using the same RDS instance and thus the same database, where the user's information is stored.
```

### Change the profil picture

* Observations ?

```text
When changing the profile picture on the first instance, the change is not reflected on the second one, and the server returns a 404 error when trying to load it. This is due to the fact that the profile picture is stored on the instance's file system and not in the database, and as a result it is not shared between the two instances.
```
