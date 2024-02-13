[![Python application](https://github.com/MatveyIvanov/Verim-Back/actions/workflows/python-app.yml/badge.svg)](https://github.com/MatveyIvanov/Verim-Back/actions/workflows/python-app.yml)


```bash
python -m grpc_tools.protoc -I /protobufs --python_out=. --grpc_python_out=. /protobufs/auth.proto
python -m grpc_tools.protoc -I /protobufs --python_out=. --grpc_python_out=. /protobufs/publisher.proto
```
