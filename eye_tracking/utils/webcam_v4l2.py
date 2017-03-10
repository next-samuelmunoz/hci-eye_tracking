# -*- coding: utf-8 -*-
"""Use webcam with v4l2capture.
This package allows to get the full camera resolution.
From:
https://github.com/gebart/python-v4l2capture/blob/master/capture_picture.py

Required package libv4l-dev
"""

import select
from threading import Thread

from PIL import Image
import v4l2capture


class WebcamThread(Thread):

    def __init__(self, device, width, height, color='RGB'):
        '''Intialize device
        '''
        self.color = color
        self._cam = v4l2capture.Video_device(device)
        self.width, self.height = self._cam.set_format(width, height)
        self.running = True
        self.img = None
        Thread.__init__(self)


    def run(self):
        '''Thread loop. Read continuously from cam buffer.
        '''
        self._cam.create_buffers(1)
        self._cam.queue_all_buffers()
        self._cam.start()
        while self.running:
            select.select((self._cam,), (), ())
            self.img = self._cam.read_and_queue()
        self._cam.close()


    def capture(self, path_file):
        '''Capture image into a file
        '''
        image = Image.frombytes(self.color, (self.width, self.height), self.img)
        image.save(path_file)


    def get_img(self):
        image = Image.frombytes(self.color, (self.width, self.height), self.img)
        return (image.tobytes(), image.size, image.mode)


    def close(self):
        '''Stop webcam and thread
        '''
        self.running = False


class Webcam(object):
    '''Wrapper over the thread.
    '''

    def __init__(self, *args, **kwargs):
        self.thread = WebcamThread(*args, **kwargs)
        self.thread.start()

    def capture(self, *args, **kwargs):
        self.thread.capture(*args, **kwargs)

    def get_img(self, *args, **kwargs):
        return self.thread.get_img(*args, **kwargs)

    def close(self):
        self.thread.close()
        self.thread.join()



if __name__ == "__main__":
    import os
    file_names = [x for x in os.listdir("/dev") if x.startswith("video")]
    file_names.sort()
    for file_name in file_names:
        path = "/dev/" + file_name
        print path
        try:
            video = v4l2capture.Video_device(path)
            driver, card, bus_info, capabilities = video.get_info()
            print "    driver:       %s\n    card:         %s" \
                "\n    bus info:     %s\n    capabilities: %s" % (
                    driver, card, bus_info, ", ".join(capabilities))
            video.close()
        except IOError, e:
            print "    " + str(e)
