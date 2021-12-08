import board
import busio

from depthglove import DepthGlove
    
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

import time
import numpy as np
import cv2
import sys

from PIL import Image

try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
    except:
        from pylibfreenect2 import CpuPacketPipeline
        pipeline = CpuPacketPipeline()

print("Packet pipeline: ", type(pipeline).__name__)

if __name__ == '__main__':
    
    depthglove = DepthGlove()

    fn = Freenect2()
    num_devices = fn.enumerateDevices()
    if num_devices == 0:
        print("No device connected!")
        sys.exit(1)

    serial = fn.getDeviceSerialNumber(0)
    device = fn.openDevice(serial, pipeline=pipeline)

    listener = SyncMultiFrameListener(FrameType.Ir | FrameType.Depth)

    #device.setColorFrameListener(listener)
    device.setIrAndDepthFrameListener(listener)

    device.start()

    registration = Registration(device.getIrCameraParams(),
                                device.getColorCameraParams())

    undistorted = Frame(512, 424, 4)
    registered = Frame(512, 424, 4)

    need_bigdepth = False
    need_color_depth_map = False

    bigdepth = Frame(1920, 1082, 4) if need_bigdepth else None
    color_depth_map = np.zeros((424, 512), np.int32).ravel() if need_color_depth_map else None

    try:
        while True:
            frames = listener.waitForNewFrame()
            start = time.time()
            print("received new frame")

            #color = frames["color"]
            #ir = frames["ir"]
            depth = frames["depth"]
            print("got depth frame at {}".format(time.time()-start))

            #registration.apply(color, depth, undistorted, registered,
            #                   bigdepth=bigdepth,
            #                   color_depth_map=color_depth_map)

            #cv2.imshow("ir", ir.asarray() / 65535.)
            #cv2.imshow("depth", depth.asarray() / 4500.)
            print("displayed image at {}".format(time.time()-start))
            
            #print(depth.asarray().shape)
            #input()
            
            depthglove.update_glove(depth.asarray())
            print("glove updated at {}".format(time.time()-start))
            #cv2.imshow("color", cv2.resize(color.asarray(),
            #                                (int(1920 / 3), int(1080 / 3))))
            #cv2.imshow("registered", registered.asarray(np.uint8))

            #print("depth first element: ", depth.asarray()[0])

            listener.release(frames)

            key = cv2.waitKey(delay=1)
            if key == ord('q'):
                break

            #time.sleep(1)
    except KeyboardInterrupt:
        depthglove.stop_fingers()
        device.stop()
        device.close()

        sys.exit(0)
    
    
    
        
        
