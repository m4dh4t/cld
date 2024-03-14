# Database migration

In this task you will migrate the Drupal database to the new RDS database instance.

![Schema](./img/CLD_AWS_INFA.PNG)

## Task 01 - Securing current Drupal data

### [Get Bitnami MariaDb user's password](https://docs.bitnami.com/aws/faq/get-started/find-credentials/)

```bash
[INPUT]
cat /home/bitnami/bitnami_credentials

[OUTPUT]
Welcome to the Bitnami package for Drupal

******************************************************************************
The default username and password is 'user' and 'J/tuoaYBysx9'.
******************************************************************************

You can also use this password to access the databases and any other component the stack includes.

Please refer to https://docs.bitnami.com/ for more details.
```

### Get Database Name of Drupal

```bash
[INPUT]
mariadb -u root -pJ/tuoaYBysx9
show databases;

[OUTPUT]
+--------------------+
| Database           |
+--------------------+
| bitnami_drupal     |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
6 rows in set (0.003 sec)
```

### [Dump Drupal DataBases](https://mariadb.com/kb/en/mariadb-dump/)

```bash
[INPUT]
mariadb-dump bitnami_drupal -u root -pJ/tuoaYBysx9 > bitnami_drupal.sql
head bitnami_drupal.sql

[OUTPUT]
-- MariaDB dump 10.19-11.2.3-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bitnami_drupal
-- ------------------------------------------------------
-- Server version       11.2.3-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
[...]
```

### Create the new Data base on RDS

```sql
[INPUT]
CREATE DATABASE bitnami_drupal;
```

### [Import dump in RDS db-instance](https://mariadb.com/kb/en/restoring-data-from-dump-files/)

Note : you can do this from the Drupal Instance. Do not forget to set the "-h" parameter.

```sql
[INPUT]
mariadb -h dbi-devopsteam15.cshki92s4w5p.eu-west-3.rds.amazonaws.com -u admin -pDEVOPSTEAM15! bitnami_drupal < bitnami_drupal.sql

[NO OUTPUT]
```

### [Get the current Drupal connection string parameters](https://www.drupal.org/docs/8/api/database-api/database-configuration)

```bash
[INPUT]
tail -n 15 /opt/bitnami/drupal/sites/default/settings.php

[OUTPUT]
[...]
'username' => 'bn_drupal',
'password' => '0d5865165bf72d263b00e2e6df91e0b5994f7bf6f2961b4d1bc2d5f5694c86fd',
[...]
```

### Replace the current host with the RDS FQDN

```php
//settings.php

$databases['default']['default'] = array (
   [...] 
  'host' => 'dbi-devopsteam15.cshki92s4w5p.eu-west-3.rds.amazonaws.com',
   [...] 
);
```

### [Create the Drupal Users on RDS Data base](https://mariadb.com/kb/en/create-user/)

Note : only calls from both private subnets must be approved.

* [By Password](https://mariadb.com/kb/en/create-user/#identified-by-password)
* [Account Name](https://mariadb.com/kb/en/create-user/#account-names)
* [Network Mask](https://cric.grenoble.cnrs.fr/Administrateurs/Outils/CalculMasque/)

```sql
[INPUT]
CREATE USER bn_drupal@'10.0.15.0/255.255.255.240' IDENTIFIED BY '0d5865165bf72d263b00e2e6df91e0b5994f7bf6f2961b4d1bc2d5f5694c86fd';

GRANT ALL PRIVILEGES ON bitnami_drupal.* TO bn_drupal@'10.0.15.0/255.255.255.240';

FLUSH PRIVILEGES;
```

```sql
[INPUT]
SHOW GRANTS for bn_drupal@'10.0.15.0/255.255.255.240';

[OUTPUT]
+----------------------------------------------------------------------------------------------------------------------------------+
| Grants for bn_drupal@10.0.15.0/255.255.255.240                                                                                   |
+----------------------------------------------------------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `bn_drupal`@`10.0.15.0/255.255.255.240` IDENTIFIED BY PASSWORD '*DE5E596666A380304A5432BC7D04C88109E3520C' |
| GRANT ALL PRIVILEGES ON `bitnami_drupal`.* TO `bn_drupal`@`10.0.15.0/255.255.255.240`                                            |
+----------------------------------------------------------------------------------------------------------------------------------+
```

### Validate access (on the drupal instance)

```sql
[INPUT]
mysql -h dbi-devopsteam15.cshki92s4w5p.eu-west-3.rds.amazonaws.com -u bn_drupal -p0d5865165bf72d263b00e2e6df91e0b5994f7bf6f2961b4d1bc2d5f5694c86fd

[INPUT]
show databases;

[OUTPUT]
+--------------------+
| Database           |
+--------------------+
| bitnami_drupal     |
| information_schema |
+--------------------+
2 rows in set (0.001 sec)
```

* Repeat the procedure to enable the instance on subnet 2 to also talk to your RDS instance.
