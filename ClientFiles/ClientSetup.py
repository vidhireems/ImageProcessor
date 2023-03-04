import subprocess
import sys

# Install gRPC and its tools using pip
subprocess.call(f"{sys.executable} -m pip install grpcio", shell=True)
subprocess.call(f"{sys.executable} -m pip install grpcio-tools", shell=True)
subprocess.call(f"{sys.executable} -m pip install Pillow")

# Run proto buf to create the stub from ImageProcessor.proto
subprocess.call(f"{sys.executable} -m grpc_tools.protoc -I./protos --python_out=./protos --grpc_python_out=./protos ./protos/ImageProcessor.proto", shell=True)