import io
import grpc
from concurrent import futures
from PIL import Image
import sys 
import os
sys.path.append(os.path.join("..", "protos"))
import ImageProcessor_pb2
import traceback
import ImageProcessor_pb2_grpc
from ImageProcessorFactory import ImageProcessFactory
from ImageProcessorCommand import *


'''
                    Pipe-Filter Architecture
    Creates list of filters based on operations list and appended
    to pipe. Each operation is considered as command. Hence, each
    command and filter are used interchangeably. 
'''
class ImageProcessorPipeline:
    def __init__(self, operations):
        self.commands = []
        self.operations = operations
    
    #Creates a list of operations(or filters) and appends to pipe
    def createPipe(self):
        try:
            for op in self.operations:
                if op.operationType == 'flip':
                    flipDirection = op.flip.direction
                    if  flipDirection == ImageProcessor_pb2.FlipDirection.HORIZONTAL:
                        self.commands.append(FlipCommand(ImageProcessFactory.getOperation(op.operationType, True)))
                    else:
                        self.commands.append(FlipCommand(ImageProcessFactory.getOperation(op.operationType, False)))
                elif op.operationType == 'gray':
                    self.commands.append(GrayScaleCommand(ImageProcessFactory.getOperation(op.operationType)))
                elif op.operationType == 'rotate':
                    self.commands.append(RotateCommand(ImageProcessFactory.getOperation(op.operationType, op.rotate.angle)))
                elif op.operationType == 'resize':
                    self.commands.append(ResizeCommand(ImageProcessFactory.getOperation(op.operationType, (op.resize.width, op.resize.height))))
                elif op.operationType == 'thumbnail':
                    self.commands.append(ThumbnailCommand(ImageProcessFactory.getOperation(op.operationType, (op.thumbnail.width, op.thumbnail.height))))
                else:
                    raise NotImplementedError("Invalid operation type: " + op.operationType)   
        except NotImplementedError as e:
            raise e
        except Exception as e:
            raise e


    #Processes each filter(or commands) in the list and stores the resultant image             
    def process(self, img, processedImg):
        try:
            for cmd in self.commands:
                if isinstance(cmd, ThumbnailCommand):
                    processedImg.append(cmd.execute(img))
                else:
                    img = cmd.execute(img)
            processedImg.append(img)
            return processedImg
        except NotImplementedError as e:
            raise e
        except Exception as e:
            raise e
    

#Image processing service implementation
class ImageProcessorServicerImpl(ImageProcessor_pb2_grpc.ImageProcessorServicer):
    """
        Process an image using a pipeline of image processing operations.

        Request:
        - image: bytes - the image to process, in JPEG format
        - operations: List[str] - a list of operations to apply to the image

        Response:
        - image: bytes - the processed image, in JPEG format

        Raises:
        - grpc.RpcError: if an error occurs while processing the image
    """
    def processImage(self, request, context):
        try:

            # Convert image bytes to Pillow image
            img = Image.open(io.BytesIO(request.image))
            imageType =  request.imageType.lower()
            if imageType is None:
                raise ValueError("invalid input image type")
            if imageType != 'jpg' and imageType != 'png':
                raise NotImplementedError("The provided image format is not supported")
            if imageType == 'jpg':
                imageType = 'jpeg'
            #Processes image based on Pipe-Filter architecture
            processedImg = []
            pipeline = ImageProcessorPipeline(request.operations)
            pipeline.createPipe()
            processedImg = pipeline.process(img, processedImg)
            
            # Convert Pillow image to bytes
            processedImgBytes = []
            for img in processedImg:
                imgBytes = io.BytesIO()
                img.save(imgBytes, format=imageType)
                imgBytes = imgBytes.getvalue()
                processedImgBytes.append(imgBytes)

            # Send image back to the client
            response = ImageProcessor_pb2.ProcessImageResponse(image=processedImgBytes)
            return response
        except ValueError as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))
            return ImageProcessor_pb2.ProcessImageResponse()
        except OSError as e:
            context.abort(grpc.StatusCode.DATA_LOSS, str(e))
        except MemoryError as e:
            context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, str(e))
        except NotImplementedError as e:
            context.abort(grpc.StatusCode.UNIMPLEMENTED, str(e))
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
            return ImageProcessor_pb2.ProcessImageResponse()

#Creates a blocking server to provide image processing services
def serve():
    #gRPC server can handle up to 10 concurrent requests in parallel
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ImageProcessor_pb2_grpc.add_ImageProcessorServicer_to_server(ImageProcessorServicerImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

#Starts the server
if __name__ == '__main__':
    serve()