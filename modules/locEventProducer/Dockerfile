FROM python:3.9

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
RUN  python3 -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ locEvent.proto
CMD ["python", "main.py"]
