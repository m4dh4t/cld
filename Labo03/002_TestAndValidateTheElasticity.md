# Task 003 - Test and validate the elasticity

![Schema](./img/CLD_AWS_INFA.PNG)

## Simulate heavy load to trigger a scaling action

* [Install the package "stress" on your Drupal instance](https://www.geeksforgeeks.org/linux-stress-command-with-examples/)

* [Install the package htop on your Drupal instance](https://www.geeksforgeeks.org/htop-command-in-linux-with-examples/)

* Check how many vCPU are available (with htop command)

```bash
[INPUT]
htop

[OUTPUT]
    0[||                      2.6%]   Tasks: 31, 410 thr; 1 running
    1[                        0.0%]   Load average: 0.00 0.00 0.00 
  Mem[|||||||||||||||||||250M/951M]   Uptime: 04:45:57
  Swp[|                 1.25M/635M]
```

This output shows that the instance has 2 vCPUs and 951MB of RAM.

### Stress your instance

```bash
[INPUT]
stress --cpu 8 --io 4 --vm 2 --vm-bytes 128M --timeout 360s

[OUTPUT]
    0[|||||||||||||||||||||||||||||||||100.0%]   Tasks: 49, 410 thr; 2 running
    1[|||||||||||||||||||||||||||||||||100.0%]   Load average: 4.41 1.12 0.38 
  Mem[||||||||||||||||||||||||||||||363M/951M]   Uptime: 04:53:17
  Swp[|                            1.25M/635M]
```

* (Scale-IN) Observe the autoscaling effect on your infa

[Cloud watch metric](./img/CLD_AWS_CLOUDWATCH_CPU_METRICS_HIGH.png)

[Ec2 instances list (running state)](./img/CLD_AWS_EC2_LIST_HIGH.png)

```
//TODO Validate that the various instances have been distributed between the two available az.
[INPUT]
aws ec2 describe-instances \
--filters "Name=tag:Name,Values=AUTO_EC2_PRIVATE_DRUPAL_DEVOPSTEAM15" \
--query "Reservations[*].Instances[*].[InstanceId,Placement.AvailabilityZone]"

[OUTPUT]
---------------------------------------
|          DescribeInstances          |
+----------------------+--------------+
|  i-0892eca038efd25b7 |  eu-west-3a  |
|  i-0df9ae6304a15da2d |  eu-west-3a  |
|  i-00f35a130891a94be |  eu-west-3b  |
|  i-0292bbabd6783854d |  eu-west-3b  |
|  i-08f9646f5a88e0be6 |  eu-west-3b  |
+----------------------+--------------+
```

[Activity history](./img/CLD_AWS_ASG_ACTIVITY_HISTORY_ALARMHIGH.png)

[Alarm target tracking](./img/CLD_AWS_CLOUDWATCH_ALARMHIGH_STATS.png)


* (Scale-OUT) As soon as all 4 instances have started, end stress on the main machine.

[Change the default cooldown period](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scaling-cooldowns.html)

[Cloud watch metric](./img/CLD_AWS_CLOUDWATCH_CPU_METRICS_LOW.png)

[EC2 instances list (terminated state)](./img/CLD_AWS_EC2_LIST_LOW.png)

[Activity history](./img/CLD_AWS_ASG_ACTIVITY_HISTORY_ALARMLOW.png)

## Release Cloud resources

Once you have completed this lab release the cloud resources to avoid
unnecessary charges:

* Terminate the EC2 instances.
  * Make sure the attached EBS volumes are deleted as well.
* Delete the Auto Scaling group.
* Delete the Elastic Load Balancer.
* Delete the RDS instance.

(this last part does not need to be documented in your report.)

## Delivery

Inform your teacher of the deliverable on the repository (link to the commit to retrieve)
