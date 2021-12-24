import grpc
import datetime
import locEvent_pb2
import locEvent_pb2_grpc

"""
Produce and send some examplary locaction event data
"""

print("Send payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = locEvent_pb2_grpc.LocEventServiceStub(channel)

LocEvent1 = locEvent_pb2.LocEventMessage(
    creation_time=datetime.datetime.now().isoformat(),
    person_id=1,
    latitude=-100,
    longitude=30
)

LocEvent2 = locEvent_pb2.LocEventMessage(
    creation_time=datetime.datetime.now().isoformat(),
    person_id=5,
    latitude=-90,
    longitude=45
)

LocEvent3 = locEvent_pb2.LocEventMessage(
    creation_time=datetime.datetime.now().isoformat(),
    person_id=6,
    latitude=-90,
    longitude=46
)

LocEvent4 = locEvent_pb2.LocEventMessage(
    creation_time=datetime.datetime.now().isoformat(),
    person_id=8,
    latitude=-90,
    longitude=40
)

LocEvent5 = locEvent_pb2.LocEventMessage(
    creation_time=datetime.datetime.now().isoformat(),
    person_id=9,
    latitude=-80,
    longitude=50
)

result1 = stub.Create(LocEvent1)
result2 = stub.Create(LocEvent2)
result3 = stub.Create(LocEvent3)
result4 = stub.Create(LocEvent4)
result5 = stub.Create(LocEvent5)

print("Location test data sent...")
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)

