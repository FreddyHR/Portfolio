#!/bin/bash

# Variables
local_project_dir="/Users/vanderslof/Documents/Python/Projects/Kafka_Stock_Market_Project"
publicip="16.16.24.220"
keypair="KSMP_Key.pem"
kafka_version="kafka_2.12-3.5.1"
java_version="java-1.8.0-amazon-corretto-devel"
EC2_command='ssh -i "KSMP_Key.pem" ec2-user@ec2-16-16-24-220.eu-north-1.compute.amazonaws.com'

# Starting Zoo-Keeper:
# -------------------------------
echo "Starting Zoo-Keeper!"
sleep 2
osascript -e 'tell application "Terminal" to do script ""'
osascript -e 'tell application "Terminal" to do script "printf \"\\033]0;Zoo-Keeper\\007\"" in window 2'
osascript -e 'tell application "Terminal" to do script "echo \"Starting Zoo-Keeper!"" in window 2' 
osascript -e 'tell application "Terminal" to do script "ssh -i \"KSMP_Key.pem\" ec2-user@ec2-16-16-24-220.eu-north-1.compute.amazonaws.com \"cd kafka_2.12-3.5.1 && bin/zookeeper-server-start.sh config/zookeeper.properties\"" in window 2'

# Starting Kafka-Server:
# -------------------------------
osascript -e 'tell application "Terminal" to do script ""'
osascript -e 'tell application "Terminal" to do script "printf \"\\033]0;Kafka-Server\\007\"" in window 2'
osascript -e 'tell application "Terminal" to do script "sleep 10" in window 2'

## Modifying server.properties files to use EC2 publicIP
eval "$EC2_command" << EOF
    echo "Modifying server.properties file!"
    cd kafka_2.12-3.5.1
    sed -i "s|^#advertised.listeners=PLAINTEXT://your.host.name:9092|advertised.listeners=PLAINTEXT://$publicip:9092|" config/server.properties
EOF

osascript -e 'tell application "Terminal" to do script "cd /Users/vanderslof/Documents/Python/Projects/Kafka_Stock_Market_Project" in window 2' 
osascript -e 'tell application "Terminal" to do script "echo \"Starting Kafka-Server!\"" in window 2' 
osascript -e 'tell application "Terminal" to do script "sleep 2" in window 2' 
osascript -e 'tell application "Terminal" to do script "ssh -i \"KSMP_Key.pem\" ec2-user@ec2-16-16-24-220.eu-north-1.compute.amazonaws.com \"cd kafka_2.12-3.5.1 && export KAFKA_HEAP_OPTS=\\\"-Xmx256M -Xms128M\\\" && bin/kafka-server-start.sh config/server.properties\"" in window 2'