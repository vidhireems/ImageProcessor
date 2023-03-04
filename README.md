# ImageProcessor
Client-Server based Image Processor

The code is tested on windows 11 and ubuntu 22.04 separately. It is assumed that the system used for client or server has Python and pip installed. There are two sets of code files one for the server and the other for the client. 
To successfully compile with grpc install grpcio and grpc_tools:
	python -m pip install grpcio
	python -m pip install grpcio-tools
	python -m pip install Pillow

To autogenerate the dependency for gRPC communication based on proto file:
	python -m grpc_tools.protoc -I./protos --python_out=./protos --grpc_python_out=./protos ./protos/ImageProcessor.proto

The above steps should be performed on the client and server sides, I provided a setup python for both ends. If the ClientSetup.py and ServerSetup.py are executed it will download, import, and install all the necessary files. ClientFiles folder has all client related files and ServerFiles has all the server related files.
The server code should be executed first. It’s a blocking service that stays active until interrupted and waits for client requests. When the client request is received it serves the request and sends a response. The client is executed after the server is started. So, these two are required. To execute server and client use the following.
Server: python .\Server.py
Client: 
python .\Client.py .\input.jpg gray rotateleft rotate:-45 thumbnail:300:300 flip:h resize:200:200
OR
python .\Client.py .\input.jpg g rl r:-45 t:300:300 f:h rz:200:200
All the commands are space-separated and the arguments for each operation are colon-separated. For help use the following command:
python .\Client.py help 		OR 		python .\Client.py h


Command Line Arguments syntax:

    ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>USAGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    
    "        Flip Image Command-  flip:'dir' or f:'dir' - dir can be horizontal(h) or vertical(v)"
    "   Grayscale Image Command- gray or g"
    "      Rotate Image Command- rotate:'angle' or r:'angle' - +ve or -ve angle should be in degree"
    " Rotate Left Image Command- rotateleft or rl"
    "Rotate Right Image Command- rotateright or rr"
    "      Resize Image Command- resize:'width':'height' or rz:'width':'height'"
    "   Thumbnail Image Command- thumbnail:'width':'height' or t:'width':'height'"
    "Example- python .\Client.py .\image.jpg gray rotateleft rotate:45 thumbnail:300:300 flip:h resize:200:200"
    "Example using short form- python .\Client.py image.jpg g rl r:45 t:300:300 f:h rz:200:200 \n"
    "-> Any command can be used in any order, each command should be space separated."
    "-> The arguments in command is ':' separated. Second argument is path to the input image."
    "-> The output images are stored in same place as where this file is run"
    ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"