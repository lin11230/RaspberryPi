#! /usr/bin/python
import io
import time
import picamera

with picamera.PiCamera() as camera:
    stream = picamera.PiCameraCircularIO(camera, seconds=60)
    camera.start_preview()
    camera.start_recording(stream, format='h264')
    camera.wait_recording(1)
    camera.wait_recording(60)
    with stream.lock:
        for frame in stream.frames:
            if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                stream.seek(frame.position)
                break
        with io.open('motion.h264', 'wb') as output:
            output.write(stream.read())


    camera.stop_recording()
    camera.stop_preview()
