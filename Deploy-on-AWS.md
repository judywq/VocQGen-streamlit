## How to setup EC2 instance

``` sh
# Get docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Get the latest version of docker-compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Get git
sudo yum install -y git
```