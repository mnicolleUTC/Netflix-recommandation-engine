# Description of instruction installation that should be run 
# on the aws server to configure Web Server app
# Initiate instance with key pair and security group that allows ssh,
# http and https connection
# Set an Elastic IP
# After running ssh command to connect to the EC2 instance run following command
sudo apt-get update
# Install and initiate virtual env
sudo apt-get install -y python3 python3-pip python3-venv
# Go to app folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Copy your flask App in a new folder at the root /home/ubuntu
# Unicorn 
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
# Set inbound rule in security group to autorize access to port 8000 on your EC2 instance 
# If error when running this command : "[3612] [ERROR] Connection in use: ('0.0.0.0', 8000)"
# First debug step = Kill process that use port 8000
# sudo lsof -i :8000 # Will list PID using the port 8000
# sudo kill <pid-number>