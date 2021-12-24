from kafka import KafkaConsumer
from sqlalchemy import create_engine
import json
import os

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]


print("locEventConsumer.py started.")

try:
    consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL])
    print("Kafka consumer started successfully.")

except Exception as err:
    print("Could not establish Consumer Service.")
    print(str(err))
    exit()


def add_loc_to_db(loc):
    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    conn = engine.connect()

    person_id = int(loc["person_id"])
    latitude, longitude = int(loc["latitude"]), int(loc["longitude"])

    insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
        .format(person_id, latitude, longitude)

    print(insert)
    conn.execute(insert)


while True:
    for msg in consumer:
        loc_values = msg.value.decode('utf-8')
        print('Message received: {}'.format(loc_values))
        if all(key in loc_values for key in ("creation_time", "longitude", "latitude", "person_id")):
            loc = json.loads(loc_values)
            add_loc_to_db(loc)

