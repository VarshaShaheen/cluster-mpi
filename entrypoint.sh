#!/bin/bash

# Start SSH daemon
/usr/sbin/sshd

# Wait for all containers to be ready
sleep 5

# If this is the master node
if [ "$HOSTNAME" = "mpi-master" ]; then
    # Create the hosts file
    echo "Creating /root/hosts file on mpi-master"

    # Generate the hosts file from environment variable HOSTS
    echo "$HOSTS" | tr ',' '\n' > /root/hosts

    # Test SSH connectivity to all hosts
    for host in $(echo "$HOSTS" | tr ',' ' '); do
        hostname=$(echo $host | cut -d' ' -f1)
        if [ "$hostname" != "mpi-master" ]; then
            echo "Testing SSH to $hostname"
            while ! ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 $hostname hostname >/dev/null 2>&1; do
                echo "Waiting for SSH on $hostname..."
                sleep 2
            done
            echo "SSH to $hostname is ready"
        fi
    done
fi

# Keep the container running
tail -f /dev/null
