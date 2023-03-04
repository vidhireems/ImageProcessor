import grpc
import sys 
import os
sys.path.append(os.path.join("..", "protos"))
import ImageProcessor_pb2
import ImageProcessor_pb2_grpc
import traceback

ROTATE_COUNTER_CLOCKWISE = -90
ROTATE_CLOCKWISE = 90

#Create operation object to flip image
def flipImage(direction):
    operation = ImageProcessor_pb2.ImageProcessorOperation(
        operationType = "flip",
        flip=ImageProcessor_pb2.FlipParams(direction=direction)
    )
    return operation

#Create operation object to convert to grayscale image
def grayscaleImage():
    operation = ImageProcessor_pb2.ImageProcessorOperation(
        operationType = "gray",
        grayscale=ImageProcessor_pb2.GrayscaleParams()
    )
    return operation

#Create operation object to rotate image in any direction
def rotateImage(angle):
    operation = ImageProcessor_pb2.ImageProcessorOperation(
        operationType = "rotate",
        rotate=ImageProcessor_pb2.RotateParams(angle=-angle)
    )
    return operation

#Create operation object to rotate image in left direction
def rotateImageLeft():
    return rotateImage(ROTATE_COUNTER_CLOCKWISE)

#Create operation object to rotate image in right direction
def rotateImageRight():
    return rotateImage(ROTATE_CLOCKWISE)

#Create operation object to resize the image
def resizeImage(width, height):
    operation = ImageProcessor_pb2.ImageProcessorOperation(
        operationType = "resize",
        resize=ImageProcessor_pb2.ResizeParams(width=width, height=height)
    )
    return operation

#Create operation object to generate thumbnail of the image
def thumbnailImage(width, height):
    operation = ImageProcessor_pb2.ImageProcessorOperation(
        operationType = "thumbnail",
        thumbnail=ImageProcessor_pb2.ThumbnailParams(width=width, height=height)
    )
    return operation

#Send request to GRPC server for image processing 
def processImage(imageData, imageType, operations):

    channel = grpc.insecure_channel('localhost:50051')
    stub = ImageProcessor_pb2_grpc.ImageProcessorStub(channel)
    request = ImageProcessor_pb2.ProcessImageRequest(
        image=imageData,
        imageType=imageType,
        operations=operations,
    )

    response = stub.processImage(request)
    return response.image

# Identify each operation and parse parameters for each operation
def getOperation(operation):
    if operation == None:
        return []
    op = (operation[0]).lower()
    if op == 'flip' or op == 'f':
        if len(operation) != 2:
            raise ValueError("Incorrect syntax for flip operation")
        direction = operation[1].lower()
        if direction == 'horizontal' or direction == 'h':
            flip = flipImage(direction=ImageProcessor_pb2.FlipDirection.HORIZONTAL)
        elif direction == 'vertical' or direction == 'v':
            flip = flipImage(direction=ImageProcessor_pb2.FlipDirection.VERTICAL)
        else:
            raise ValueError("Incorrect syntax for flip operation")
        return flip
    elif op == 'gray' or op == 'g':
        return grayscaleImage()
    elif op == 'rotate' or op == 'r':
        if len(operation) != 2:
            raise ValueError("Incorrect syntax for rotate operation")
        angle = int(operation[1])
        angle = angle % 360
        return rotateImage(angle)
    elif op == 'rotateleft' or op == 'rl':
        if len(operation) != 1:
            raise ValueError("Incorrect syntax for rotate left operation")
        return rotateImageLeft()
    elif op == 'rotateright' or op == 'rr':
        if len(operation) != 1:
            raise ValueError("Incorrect syntax for rotate right operation")
        return rotateImageRight()
    elif op == 'resize' or op == 'rz':
        if len(operation) != 3:
            raise ValueError("Incorrect syntax for resize operation")
        width = int(operation[1])
        height = int(operation[2])
        return resizeImage(width, height)
    elif op == 'thumbnail' or op == 't':
        if len(operation) != 1 and len(operation) != 3:
            raise ValueError("Incorrect syntax for thumbnail operation")
        if len(operation) == 1:
            return thumbnailImage(300, 300)
        width = int(operation[1])
        height = int(operation[2])
        return thumbnailImage(width, height)
    else:
        raise ValueError("Incorrect operation provided")

# Create a list of operations
def getOperationsList():
    operations = []

    try:
        for i in range(2, len(sys.argv)):
            operation = sys.argv[i].split(':')
            operations.append(getOperation(operation))
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
        printHelp()

    return operations

#Print help for each operation
def printHelp():
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>USAGE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print()
    print("        Flip Image Command-  flip:'dir' or f:'dir' - dir can be horizontal(h) or vertical(v)")
    print("   Grayscale Image Command- gray or g")
    print("      Rotate Image Command- rotate:'angle' or r:'angle' - +ve or -ve angle should be in degree")
    print(" Rotate Left Image Command- rotateleft or rl")
    print("Rotate Right Image Command- rotateright or rr")
    print("      Resize Image Command- resize:'width':'height' or rz:'width':'height'")
    print("   Thumbnail Image Command- thumbnail:'width':'height' or t:'width':'height'")
    print("Example- python .\Client.py .\image.jpg gray rotateleft rotate:45 thumbnail:300:300 flip:h resize:200:200")
    print("Example using short form- python .\Client.py image.jpg g rl r:45 t:300:300 f:h rz:200:200 \n")
    print("-> Any command can be used in any order, each command should be space separated.")
    print("-> The arguments in command is ':' separated. Second argument is path to the input image.")
    print("-> The output images are stored in same place as where this file is run")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    exit(1)

def main():
        
    try:    
        if len(sys.argv) < 2:
            raise ValueError("No image path provided")
        
        if sys.argv[1].lower() == 'help' or sys.argv[1].lower() == 'h':
            printHelp()

        #parse the file path
        filePath = sys.argv[1]
        if not os.path.exists(filePath):
            raise ValueError("Path of the file is Invalid")
        
        imageType = filePath.split('.')[-1]

        #Read the provided image
        with open(filePath, 'rb') as f:
            imageData = f.read()

        #Parse and get a list of operations
        operations = getOperationsList()

        #Invoke remote procedures at server
        outputImageList = processImage(imageData, imageType, operations)

        #Generate the thumbnails for the image
        for i in range(len(outputImageList)-1):
            filename = "thumbnail" + str(i+1) + "." + imageType
            with open(filename, 'wb') as f:
                f.write(outputImageList[i])

        #Return the processed image
        filename = "output." + imageType
        with open(filename, 'wb') as f:
            f.write(outputImageList[-1])
        print("Image Processing was successful!")
        
    # Handle the gRPC error
    except grpc.RpcError as e:
        print("Error: {} - {}".format(e.code(), e.details()))
    # Handle the value error
    except ValueError as e:
        print("Value Error: {}".format(e))
        traceback.print_exc()
    # Handle unkknown exception
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()

#The code execution starts here
if __name__ == '__main__':
    main()