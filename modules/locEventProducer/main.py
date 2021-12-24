import time
from concurrent import futures

import grpc
import locEvent_pb2
import locEvent_pb2_grpc
from kafka import KafkaProducer
import logging
import os
import json
import datetime


kafka_url = os.environ["KAFKA_URL"]
kafka_topic = os.environ["KAFKA_TOPIC"]

logging.info('kafka_url : ', kafka_url)
logging.info('kafka_topic : ', kafka_topic)
producer = KafkaProducer(bootstrap_servers=kafka_url)

class LocEventService(locEvent_pb2_grpc.LocEventService):
    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            'creation_time': datetime.datetime.now().isoformat(),
            'person_id': int(request.person_id),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }
        print(request_value)
        user_encode_data = json.dumps(request_value, indent=2).encode('utf-8')
        producer.send(kafka_topic, user_encode_data)
        return locEvent_pb2.LocEventMessage(**request_value)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
locEvent_pb2_grpc.add_LocEventServiceServicer_to_server(LocEventService(), server)

print("Server starts on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)