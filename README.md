# Netflix-recommandation-engine
Netflix recommandation engine for Jedha final project

# How launch API
Pre-requisite : Load credidentials.py in your kafka_streaming folder  
Contact owner repository to get those credentials  

Step 1 : Launch two dockers containers (one consumer one producer) with following command : 
docker run -it -v "$(pwd):/home/app" mnicolle/netflix_recommandation

Step 2 : Lauch producer.py in one docker with following command :
python producer.py

Step 3 : Lauch consumer.py the other docker with following command :
python consumer.py

Pay attention to number of running containers if kafka consumer and producer doesn't communicate.  
It can be due to dual running containers.


### Connect to aws web server hosting the flaskAPI
1) Naviguate to ./Netflix-recommandation-engine/aws_server folder
2) Get your Netflix-project.pem key in order to access EC2 server and copy it in current directory
3) ssh -i Netflix-project.pem ubuntu@ip_adress
