# Deploy the elastic load balancer

In this task you will create a load balancer in AWS that will receive
the HTTP requests from clients and forward them to the Drupal
instances.

![Schema](./img/CLD_AWS_INFA.PNG)

## Task 01 Prerequisites for the ELB

* Create a dedicated security group

|Key|Value|
|:--|:--|
|Name|SG-DEVOPSTEAM15-LB|
|Inbound Rules|Application Load Balancer|
|Outbound Rules|Refer to the infra schema|

```bash
[INPUT]
aws ec2 create-security-group \
--vpc-id vpc-03d46c285a2af77ba \
--group-name SG-DEVOPSTEAM15-LB \
--description SG-DEVOPSTEAM15-LB

aws ec2 authorize-security-group-ingress \
--group-id sg-06d4adf554aad122f \
--protocol tcp \
--port 8080 \
--cidr 10.0.0.0/28

[OUTPUT]
-------------------------------------
|        CreateSecurityGroup        |
+----------+------------------------+
|  GroupId |  sg-06d4adf554aad122f  |
+----------+------------------------+

------------------------------------------------------------------------------------------------------------------------------------
|                                                   AuthorizeSecurityGroupIngress                                                  |
+-----------------------------------------------------------------------+----------------------------------------------------------+
|  Return                                                               |  True                                                    |
+-----------------------------------------------------------------------+----------------------------------------------------------+
||                                                       SecurityGroupRules                                                       ||
|+-------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
||  CidrIpv4   | FromPort  |        GroupId        | GroupOwnerId  | IpProtocol  | IsEgress  |   SecurityGroupRuleId   | ToPort   ||
|+-------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
||  10.0.0.0/28|  8080     |  sg-06d4adf554aad122f |  709024702237 |  tcp        |  False    |  sgr-039c6cd91c3939604  |  8080    ||
|+-------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
```

* Create the Target Group

|Key|Value|
|:--|:--|
|Target type|Instances|
|Name|TG-DEVOPSTEAM15|
|Protocol and port|Refer to the infra schema|
|Ip Address type|IPv4|
|VPC|Refer to the infra schema|
|Protocol version|HTTP1|
|Health check protocol|HTTP|
|Health check path|/|
|Port|Traffic port|
|Healthy threshold|2 consecutive health check successes|
|Unhealthy threshold|2 consecutive health check failures|
|Timeout|5 seconds|
|Interval|10 seconds|
|Success codes|200|

```bash
[INPUT]
aws elbv2 create-target-group \
--vpc-id vpc-03d46c285a2af77ba \
--name TG-DEVOPSTEAM15 \
--target-type instance \
--protocol HTTP \
--port 8080 \
--ip-address-type ipv4 \
--protocol-version HTTP1 \
--health-check-protocol HTTP \
--health-check-port traffic-port \
--health-check-path / \
--health-check-enabled \
--health-check-interval-seconds 10 \
--health-check-timeout-seconds 5 \
--healthy-threshold-count 2 \
--unhealthy-threshold-count 2 \
--matcher HttpCode=200

aws elbv2 register-targets \
--target-group-arn arn:aws:elasticloadbalancing:eu-west-3:709024702237:targetgroup/TG-DEVOPSTEAM15/9400f8739ae3066d \
--targets Id=i-024afa9ff113bc864 Id=i-07a07eb168474cc56

[OUTPUT]
--------------------------------------------------------------------------------------------------------------------------------------
|                                                          CreateTargetGroup                                                         |
+------------------------------------------------------------------------------------------------------------------------------------+
||                                                           TargetGroups                                                           ||
|+----------------------------+-----------------------------------------------------------------------------------------------------+|
||  HealthCheckEnabled        |  True                                                                                               ||
||  HealthCheckIntervalSeconds|  10                                                                                                 ||
||  HealthCheckPath           |  /                                                                                                  ||
||  HealthCheckPort           |  traffic-port                                                                                       ||
||  HealthCheckProtocol       |  HTTP                                                                                               ||
||  HealthCheckTimeoutSeconds |  5                                                                                                  ||
||  HealthyThresholdCount     |  2                                                                                                  ||
||  IpAddressType             |  ipv4                                                                                               ||
||  Port                      |  8080                                                                                               ||
||  Protocol                  |  HTTP                                                                                               ||
||  ProtocolVersion           |  HTTP1                                                                                              ||
||  TargetGroupArn            |  arn:aws:elasticloadbalancing:eu-west-3:709024702237:targetgroup/TG-DEVOPSTEAM15/9400f8739ae3066d   ||
||  TargetGroupName           |  TG-DEVOPSTEAM15                                                                                    ||
||  TargetType                |  instance                                                                                           ||
||  UnhealthyThresholdCount   |  2                                                                                                  ||
||  VpcId                     |  vpc-03d46c285a2af77ba                                                                              ||
|+----------------------------+-----------------------------------------------------------------------------------------------------+|
|||                                                             Matcher                                                            |||
||+--------------------------------------------------------------------------------+-----------------------------------------------+||
|||  HttpCode                                                                      |  200                                          |||
||+--------------------------------------------------------------------------------+-----------------------------------------------+||
```

## Task 02 Deploy the Load Balancer

[Source](https://aws.amazon.com/elasticloadbalancing/)

* Create the Load Balancer

|Key|Value|
|:--|:--|
|Type|Application Load Balancer|
|Name|ELB-DEVOPSTEAM15|
|Scheme|Internal|
|Ip Address type|IPv4|
|VPC|Refer to the infra schema|
|Security group|Refer to the infra schema|
|Listeners Protocol and port|Refer to the infra schema|
|Target group|Your own target group created in task 01|

Provide the following answers (leave any
field not mentioned at its default value):

```bash
[INPUT]
aws elbv2 create-load-balancer \
--type application \
--name ELB-DEVOPSTEAM15 \
--scheme internal \
--ip-address-type ipv4 \
--subnets subnet-0598517fbbd15df52 subnet-016d3f0da8ee1a2b5 \
--security-groups sg-06d4adf554aad122f

aws elbv2 create-listener \
--load-balancer-arn arn:aws:elasticloadbalancing:eu-west-3:709024702237:loadbalancer/app/ELB-DEVOPSTEAM15/0ab2f03733ddb563 \
--protocol HTTP \
--port 8080 \
--default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:eu-west-3:709024702237:targetgroup/TG-DEVOPSTEAM15/9400f8739ae3066d

# Update the security group of the EC2 instances, to allow the ELB to communicate with them
# LB TRAFFIC - AZ1
aws ec2 authorize-security-group-ingress \
--group-id sg-03f583e7906065891 \
--protocol tcp \
--port 8080 \
--cidr 10.0.15.0/28
# LB TRAFFIC - AZ2
aws ec2 authorize-security-group-ingress \
--group-id sg-03f583e7906065891 \
--protocol tcp \
--port 8080 \
--cidr 10.0.15.128/28

[OUTPUT]
---------------------------------------------------------------------------------------------------------------------------------------
|                                                         CreateLoadBalancer                                                          |
+-------------------------------------------------------------------------------------------------------------------------------------+
||                                                           LoadBalancers                                                           ||
|+-----------------------+-----------------------------------------------------------------------------------------------------------+|
||  CanonicalHostedZoneId|  Z3Q77PNBQS71R4                                                                                           ||
||  CreatedTime          |  2024-03-21T14:21:43.780000+00:00                                                                         ||
||  DNSName              |  internal-ELB-DEVOPSTEAM15-157476931.eu-west-3.elb.amazonaws.com                                          ||
||  IpAddressType        |  ipv4                                                                                                     ||
||  LoadBalancerArn      |  arn:aws:elasticloadbalancing:eu-west-3:709024702237:loadbalancer/app/ELB-DEVOPSTEAM15/0ab2f03733ddb563   ||
||  LoadBalancerName     |  ELB-DEVOPSTEAM15                                                                                         ||
||  Scheme               |  internal                                                                                                 ||
||  Type                 |  application                                                                                              ||
||  VpcId                |  vpc-03d46c285a2af77ba                                                                                    ||
|+-----------------------+-----------------------------------------------------------------------------------------------------------+|
|||                                                        AvailabilityZones                                                        |||
||+-------------------------------------+-------------------------------------------------------------------------------------------+||
|||  SubnetId                           |  subnet-016d3f0da8ee1a2b5                                                                 |||
|||  ZoneName                           |  eu-west-3b                                                                               |||
||+-------------------------------------+-------------------------------------------------------------------------------------------+||
|||                                                        AvailabilityZones                                                        |||
||+-------------------------------------+-------------------------------------------------------------------------------------------+||
|||  SubnetId                           |  subnet-0598517fbbd15df52                                                                 |||
|||  ZoneName                           |  eu-west-3a                                                                               |||
||+-------------------------------------+-------------------------------------------------------------------------------------------+||
|||                                                         SecurityGroups                                                          |||
||+---------------------------------------------------------------------------------------------------------------------------------+||
|||  sg-06d4adf554aad122f                                                                                                           |||
||+---------------------------------------------------------------------------------------------------------------------------------+||
|||                                                              State                                                              |||
||+------------------------------------------+--------------------------------------------------------------------------------------+||
|||  Code                                    |  provisioning                                                                        |||
||+------------------------------------------+--------------------------------------------------------------------------------------+||

----------------------------------------------------------------------------------------------------------------------------------------------
|                                                               CreateListener                                                               |
+--------------------------------------------------------------------------------------------------------------------------------------------+
||                                                                 Listeners                                                                ||
|+-----------------+------------------------------------------------------------------------------------------------------------------------+|
||  ListenerArn    |  arn:aws:elasticloadbalancing:eu-west-3:709024702237:listener/app/ELB-DEVOPSTEAM15/0ab2f03733ddb563/eab27686e32264a7   ||
||  LoadBalancerArn|  arn:aws:elasticloadbalancing:eu-west-3:709024702237:loadbalancer/app/ELB-DEVOPSTEAM15/0ab2f03733ddb563                ||
||  Port           |  8080                                                                                                                  ||
||  Protocol       |  HTTP                                                                                                                  ||
|+-----------------+------------------------------------------------------------------------------------------------------------------------+|
|||                                                             DefaultActions                                                             |||
||+-------------------+--------------------------------------------------------------------------------------------------------------------+||
|||  TargetGroupArn   |  arn:aws:elasticloadbalancing:eu-west-3:709024702237:targetgroup/TG-DEVOPSTEAM15/9400f8739ae3066d                  |||
|||  Type             |  forward                                                                                                           |||
||+-------------------+--------------------------------------------------------------------------------------------------------------------+||
||||                                                             ForwardConfig                                                            ||||
|||+--------------------------------------------------------------------------------------------------------------------------------------+|||
|||||                                                     TargetGroupStickinessConfig                                                    |||||
||||+------------------------------------------------------------------------+-----------------------------------------------------------+||||
|||||  Enabled                                                               |  False                                                    |||||
||||+------------------------------------------------------------------------+-----------------------------------------------------------+||||
|||||                                                            TargetGroups                                                            |||||
||||+------------------+-----------------------------------------------------------------------------------------------------------------+||||
|||||  TargetGroupArn  |  arn:aws:elasticloadbalancing:eu-west-3:709024702237:targetgroup/TG-DEVOPSTEAM15/9400f8739ae3066d               |||||
|||||  Weight          |  1                                                                                                              |||||
||||+------------------+-----------------------------------------------------------------------------------------------------------------+||||

------------------------------------------------------------------------------------------------------------------------------------
|                                                   AuthorizeSecurityGroupIngress                                                  |
+-----------------------------------------------------------------------+----------------------------------------------------------+
|  Return                                                               |  True                                                    |
+-----------------------------------------------------------------------+----------------------------------------------------------+
||                                                       SecurityGroupRules                                                       ||
|+-------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
||  CidrIpv4   | FromPort  |        GroupId        | GroupOwnerId  | IpProtocol  | IsEgress  |   SecurityGroupRuleId   | ToPort   ||
|+-------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
|| 10.0.15.0/28|  8080     |  sg-03f583e7906065891 |  709024702237 |  tcp        |  False    |  sgr-01f3269652e62635e  |  8080    ||
|+-------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|

--------------------------------------------------------------------------------------------------------------------------------------
|                                                   AuthorizeSecurityGroupIngress                                                    |
+-----------------------------------------------------------------------+------------------------------------------------------------+
|  Return                                                               |  True                                                      |
+-----------------------------------------------------------------------+------------------------------------------------------------+
||                                                       SecurityGroupRules                                                         ||
|+---------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
||  CidrIpv4     | FromPort  |        GroupId        | GroupOwnerId  | IpProtocol  | IsEgress  |   SecurityGroupRuleId   | ToPort   ||
|+---------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
|| 10.0.15.128/28|  8080     |  sg-03f583e7906065891 |  709024702237 |  tcp        |  False    |  sgr-09fa08665459ea85e  |  8080    ||
|+---------------+-----------+-----------------------+---------------+-------------+-----------+-------------------------+----------+|
```

* Get the ELB FQDN (DNS NAME - A Record)

```bash
[INPUT]
aws elbv2 describe-load-balancers --names ELB-DEVOPSTEAM15 --query 'LoadBalancers[].DNSName'

[OUTPUT]
---------------------------------------------------------------------
|                       DescribeLoadBalancers                       |
+-------------------------------------------------------------------+
|  internal-ELB-DEVOPSTEAM15-157476931.eu-west-3.elb.amazonaws.com  |
+-------------------------------------------------------------------+
```

* Get the ELB deployment status

Note : In the EC2 console select the Target Group. In the
       lower half of the panel, click on the **Targets** tab. Watch the
       status of the instance go from **unused** to **initial**.

* Ask the DMZ administrator to register your ELB with the reverse proxy via the private teams channel

* Update your string connection to test your ELB and test it

```bash
# .ssh/config

Host cld-srv-web
  HostName 15.188.43.46
  IdentityFile ~/.ssh/cld_dmz
  User devopsteam15
  LocalForward 8080 internal-ELB-DEVOPSTEAM15-157476931.eu-west-3.elb.amazonaws.com:8080
```

```bash
ssh cld-srv-web
```

* Test your application through your ssh tunneling

```bash
[INPUT]
curl localhost:8080

[OUTPUT]
<!DOCTYPE html>
<html lang="en" dir="ltr" style="--color--primary-hue:202;--color--primary-saturation:79%;--color--primary-lightness:50">
  <head>
    <meta charset="utf-8" />
<meta name="Generator" content="Drupal 10 (https://www.drupal.org)" />
<meta name="MobileOptimized" content="width" />
<meta name="HandheldFriendly" content="true" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" href="/core/themes/olivero/favicon.ico" type="image/vnd.microsoft.icon" />
<link rel="alternate" type="application/rss+xml" title="" href="http://localhost:8080/rss.xml" />
<link rel="alternate" type="application/rss+xml" title="" href="http://localhost/rss.xml" />
    <title>Welcome! | My blog</title>
...
```

### Questions - Analysis

* On your local machine resolve the DNS name of the load balancer into
  an IP address using the `nslookup` command (works on Linux, macOS and Windows). Write
  the DNS name and the resolved IP Address(es) into the report.

  ```bash
  ❯ nslookup devopsteam15.cld.education
  ...

  Non-authoritative answer:
  Name:	devopsteam15.cld.education
  Address: 15.188.43.46
  ```

  The DNS name is `devopsteam15.cld.education` and the resolved IP address is `15.188.43.46`, which is the same IP address as the DMZ server, as the reverse proxy is hosted on the same instance. The forwarding logic is effectively hidden from the client, as to determine the destination of the request and forward it to the correct Load Balancer, the reverse proxy uses the Host header of the HTTP request (which is `devopsteam15.cld.education` in this case).

* From your Drupal instance, identify the ip from which requests are sent by the Load Balancer.

  Help : execute `tcpdump port 8080`

  ```text
  16:25:29.419092 IP 10.0.15.4.47300 > provisioner-local.http-alt: Flags [P.], seq 0:130, ack 1, win 106, options [nop,nop,TS val 3790038117 ecr 1499668646], length 130: HTTP: GET / HTTP/1.1
  16:25:28.508159 IP 10.0.15.139.31666 > provisioner-local.http-alt: Flags [P.], seq 0:130, ack 1, win 106, options [nop,nop,TS val 244139739 ecr 2511880083], length 130: HTTP: GET / HTTP/1.1
  ```

  The requests are sent from two different IP addresses: `10.0.15.4`, which is in availability zone `eu-west-3a`, and `10.0.15.139`, which is in availability zone `eu-west-3b`. This is because we chose an Application Load Balancer, which performs cross-zone load balancing by default.

* In the Apache access log identify the health check accesses from the
  load balancer and copy some samples into the report.

  ```text
  10.0.15.139 - - [21/Mar/2024:17:07:10 +0000] "GET / HTTP/1.1" 200 5151
  10.0.15.4 - - [21/Mar/2024:17:07:11 +0000] "GET / HTTP/1.1" 200 5151
  ```

  The health check accesses are correctly made through the Load Balancer, as the IP addresses are the same as the ones identified in the previous question. The logs match the configuration set for the Target Group health check, which is a GET request to `/` expecting a 200 status code, which validates that the instances are working correctly.
