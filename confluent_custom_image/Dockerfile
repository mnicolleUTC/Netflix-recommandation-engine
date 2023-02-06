# Run Jedha's Kafka confluent image
# plus install scikit-surprise module to load pickle model
FROM jedha/confluent-image
RUN apt-get update
RUN apt-get install gcc -y
RUN pip install scikit-surprise