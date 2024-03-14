* What is the smallest and the biggest instance type (in terms of
  virtual CPUs and memory) that you can choose from when creating an
  instance?

```
The smallest instance type is t2.nano with 1 vCPU and 0.5 GiB of memory.
The biggest instance type is u-6tb1.112xlarge with 448 vCPUs and 6144 GiB of memory.
```

* How long did it take for the new instance to get into the _running_
  state?

```
It was almost instantaneous.
```

* Using the commands to explore the machine listed earlier, respond to
  the following questions and explain how you came to the answer:

    * What's the difference between time here in Switzerland and the time set on the machine?

    ```
    Using `date` shows the time the machine is set to in UTC. As we are in UTC+1, the indicated time is one hour behind.
    ```

    * What's the name of the hypervisor?

    ```
    Using `lscpu` shows the name of the hypervisor as `KVM`.
    ```

    * How much free space does the disk have?

    ```
    Using `df -h` shows the file system disk space usage, in a human-readable format. The disk has 7.7G of free space. Our main filesystem `/dev/nvme0n1p1` mounted on `/` shows 6.0G of free space.
    ```

* Try to ping the instance ssh srv from your local machine. What do you see?
  Explain. Change the configuration to make it work. Ping the
  instance, record 5 round-trip times.

```
As the machine does not have a public IP address, it is not possible to ping it from the local machine and the machine can only be accessed from within the AWS network. To make it work, we need to first assign a public IP address to the machine using the `--associate-public-ip-address` option when creating the instance. Then, we need to configure the security group to allow incoming ICMP Echo Request traffic. Finally, we need to update the Route Table so that the traffic is directly routed through the Internet Gateway instead of the NAT server. The 5 round-trip times are as follows:

❯ ping 15.237.138.185
PING 15.237.138.185 (15.237.138.185): 56 data bytes
64 bytes from 15.237.138.185: icmp_seq=0 ttl=42 time=282.643 ms
64 bytes from 15.237.138.185: icmp_seq=1 ttl=42 time=73.505 ms
64 bytes from 15.237.138.185: icmp_seq=2 ttl=42 time=17.207 ms
64 bytes from 15.237.138.185: icmp_seq=3 ttl=42 time=16.849 ms
64 bytes from 15.237.138.185: icmp_seq=4 ttl=42 time=15.482 ms
^C
--- 15.237.138.185 ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 15.482/81.137/282.643/103.144 ms
```

* Determine the IP address seen by the operating system in the EC2
  instance by running the `ifconfig` command. What type of address
  is it? Compare it to the address displayed by the ping command
  earlier. How do you explain that you can successfully communicate
  with the machine?

```
bitnami@ip-10-0-15-10:~$ ip -br a
lo               UNKNOWN        127.0.0.1/8 ::1/128
ens5             UP             10.0.15.10/28 fe80::4a7:d2ff:fe21:5541/64

The non-loopback address on interface `ens5` is `10.0.15.10`, which is a private IP address. This kind of address is used to communicate within a local network and as such, it is not routable over the Internet. Because the machine has a public IP address, it does not need to be translated by the NAT server and the packets are directly routed from the local machine to the EC2 instance through the Internet Gateway.
```
