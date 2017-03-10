# Dataset Generation

**Keys:**
* ESC: quit program
* 1: target mode
* 2: webcam mode


## Installation


## Configuration



## Troubleshooting
### I can't install v4l2capture
The `v4l2capture` python package requires the v4l libraries.
```bash
apt-get install libv4l-dev
```

### Where is my webcam device?
Execute  one of the webcam modules. They should output the detected webcam devices.

```bash
$ python utils/webcam_v4l2.py
Detected webcams:
 /dev/video0
```
```bash
$ python utils/webcam_v4l2.py
/dev/video0
   driver:       uvcvideo
   card:         HP HD Camera
   bus info:     usb-0000:00:14.0-9
   capabilities: readwrite, streaming, video_capture
```

### I can't use the webcam
If you don't get a device in the previous step, add your user to the `video` group.
```bash
 usermod -a -G video <user>
 ```
