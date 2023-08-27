#!/bin/bash

# Variables
local_project_dir="/Users/vanderslof/Documents/Python/Projects/Kafka_Stock_Market_Project"
publicip="16.16.24.220"
keypair="KSMP_Key.pem"
kafka_version="kafka_2.12-3.5.1"
java_version="java-1.8.0-amazon-corretto-devel"
EC2_command='ssh -i "KSMP_Key.pem" ec2-user@ec2-16-16-24-220.eu-north-1.compute.amazonaws.com'

# Giving permissions to .pem file
# sudo chmod 400 $local_project_dir"/"$keypair

# Installing Java and Kafka
# eval "$EC2_command" << EOF
#     echo "Connected to EC2 instance!"
#     sleep 2
#     echo "Installing Java!"
#     sleep 2
#     sudo dnf install -y $java_version
#     echo "Installing Kafka!"
#     sleep 2
#     wget https://downloads.apache.org/kafka/3.5.1/$kafka_version.tgz
#     tar -xvf $kafka_version.tgz
#     sleep 2
#     # cd $kafka_version
#     # echo "Changing Kafka server configurations"
#     # sleep 2
#     # sed -i 's|^#advertised.listeners=PLAINTEXT://your.host.name:9092|advertised.listeners=PLAINTEXT://$publicip:9092|' server.properties 
# EOF
# echo "Kafka and Java installation executed on the EC2 instance!"

eval "$EC2_command" << EOF
    cd kafka_2.12-3.5.1
    sed -i "s|^#advertised.listeners=PLAINTEXT://your.host.name:9092|advertised.listeners=PLAINTEXT://$publicip:9092|" config/server.properties
EOF